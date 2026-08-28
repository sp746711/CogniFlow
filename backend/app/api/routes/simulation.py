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
analytics layer and future React dashboard can work with
dynamic data.
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
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

    The endpoint:

    1. Loads the 25 simulated developers.
    2. Loads the simulated Jira tasks and bugs.
    3. Runs the CogniFlow simulator.
    4. Generates unified developer activity events.
    5. Stores those events in PostgreSQL.
    6. Returns a summary of the generated simulation.

    No real Slack, Jira, GitHub, or IDE services are contacted.
    """

    # ----------------------------------------------------------
    # Work date
    # ----------------------------------------------------------

    if work_date is None:
        work_date = datetime.now()

    # ----------------------------------------------------------
    # Load developers
    # ----------------------------------------------------------

    developers = list(
        db.scalars(
            select(Developer)
            .order_by(Developer.id)
        ).all()
    )

    # ----------------------------------------------------------
    # Validate developer population
    # ----------------------------------------------------------

    if len(developers) != DEFAULT_CONFIG.developer_count:
        raise ValueError(
            f"CogniFlow requires "
            f"{DEFAULT_CONFIG.developer_count} developers "
            f"for simulation, but found {len(developers)}."
        )

    # ----------------------------------------------------------
    # Load tasks
    # ----------------------------------------------------------

    tasks = list(
        db.scalars(
            select(Task)
            .order_by(Task.id)
        ).all()
    )

    # ----------------------------------------------------------
    # Create simulator
    # ----------------------------------------------------------

    runner = SimulationRunner(
        config=DEFAULT_CONFIG,
    )

    # ----------------------------------------------------------
    # Generate simulated events
    # ----------------------------------------------------------

    generated_events = runner.run(
        work_date=work_date,
        developers=developers,
        tasks=tasks,
    )

    # ----------------------------------------------------------
    # Convert generated events into database events
    # ----------------------------------------------------------

    database_events: list[Event] = []

    for generated_event in generated_events:
        event = Event(
            developer_id=generated_event.developer_id,
            task_id=generated_event.task_id,
            timestamp=generated_event.timestamp,
            source=generated_event.source,
            event_type=generated_event.event_type,
            metadata=generated_event.metadata,
        )

        db.add(event)
        database_events.append(event)

    # ----------------------------------------------------------
    # Persist simulation
    # ----------------------------------------------------------

    try:
        db.commit()

    except Exception:
        db.rollback()
        raise

    # ----------------------------------------------------------
    # Return summary
    # ----------------------------------------------------------

    return {
        "message": "Simulation completed.",
        "work_date": work_date.isoformat(),
        "developers": len(developers),
        "tasks": len(tasks),
        "events_generated": len(database_events),
        "events_persisted": len(database_events),
    }