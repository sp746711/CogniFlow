"""
Simulation API routes for CogniFlow.

These endpoints generate simulated developer activity for a
CogniFlow workday.

The simulation represents activity from:

- IDE
- Slack
- Jira
- GitHub

Generated events are persisted to PostgreSQL so that the
analytics layer and dashboard can work with dynamic data.

No real external services are contacted.
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.developer import Developer
from app.models.event import Event
from app.models.task import Task
from app.simulator.config import DEFAULT_CONFIG
from app.simulator.runner import SimulationRunner


router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"],
)


@router.post("/run")
def run_simulation(
    work_date: datetime | None = None,
    db: Session = Depends(get_db),
) -> dict:
    """
    Generate and persist one simulated CogniFlow workday.

    Workflow:

    1. Load the simulated developers.
    2. Validate the expected developer population.
    3. Load simulated Jira tasks and bugs.
    4. Run the simulator.
    5. Convert GeneratedEvent objects into Event database records.
    6. Persist the events.
    7. Return a simulation summary.

    No real Slack, Jira, GitHub, or IDE services are contacted.
    """

    # ==========================================================
    # WORK DATE
    # ==========================================================

    if work_date is None:
        work_date = datetime.now()

    # ==========================================================
    # LOAD DEVELOPERS
    # ==========================================================

    developers = list(
        db.scalars(
            select(Developer).order_by(Developer.id)
        ).all()
    )

    # ==========================================================
    # VALIDATE DEVELOPERS
    # ==========================================================

    expected_developers = DEFAULT_CONFIG.developer_count

    if len(developers) != expected_developers:
        raise HTTPException(
            status_code=400,
            detail=(
                f"CogniFlow requires {expected_developers} "
                f"developers for simulation, but found "
                f"{len(developers)}."
            ),
        )

    # ==========================================================
    # LOAD TASKS
    # ==========================================================

    tasks = list(
        db.scalars(
            select(Task).order_by(Task.id)
        ).all()
    )

    if not tasks:
        raise HTTPException(
            status_code=400,
            detail=(
                "No simulated Jira tasks or bugs were found. "
                "Seed the tasks before running the simulation."
            ),
        )

    # ==========================================================
    # CREATE SIMULATOR
    # ==========================================================

    runner = SimulationRunner(
        config=DEFAULT_CONFIG,
    )

    # ==========================================================
    # GENERATE EVENTS
    # ==========================================================

    try:
        generated_events = runner.run(
            work_date=work_date,
            developers=developers,
            tasks=tasks,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # ==========================================================
    # CONVERT GENERATED EVENTS TO DATABASE EVENTS
    # ==========================================================

    database_events: list[Event] = []

    for generated_event in generated_events:
        event = Event(
            developer_id=generated_event.developer_id,
            team_id=generated_event.team_id,
            task_id=generated_event.task_id,
            timestamp=generated_event.timestamp,
            source=generated_event.source,
            event_type=generated_event.event_type,
            context=generated_event.context,
            title=generated_event.title,
            description=generated_event.description,
            related_developer_id=(
                generated_event.related_developer_id
            ),
            event_metadata=generated_event.event_metadata,
        )

        db.add(event)
        database_events.append(event)

    # ==========================================================
    # PERSIST EVENTS
    # ==========================================================

    try:
        db.commit()

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to persist simulated events.",
        ) from exc

    # ==========================================================
    # RETURN SUMMARY
    # ==========================================================

    return {
        "message": "Simulation completed.",
        "work_date": work_date.isoformat(),
        "developers": len(developers),
        "tasks": len(tasks),
        "events_generated": len(generated_events),
        "events_persisted": len(database_events),
    }