"""
Simulation API routes for CogniFlow.

These endpoints generate simulated developer activity for a
CogniFlow workday.

The simulation represents activity from:

- IDE
- Slack
- Jira
- GitHub

Generated events are persisted to PostgreSQL and then processed
through the CogniFlow analytics pipeline.

Pipeline:

    Simulator
        ↓
    Unified Events
        ↓
    EventProcessor
        ↓
    Flow Sessions
        ↓
    Interruptions
        ↓
    Context Switches
        ↓
    Recovery
        ↓
    Flow Score
        ↓
    Metrics

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
from app.services.event_processor import EventProcessor
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
    5. Convert GeneratedEvent objects into Event records.
    6. Persist the raw events.
    7. Run the EventProcessor analytics pipeline.
    8. Persist derived analytics and metrics.
    9. Return a complete simulation summary.

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
    # GENERATE SIMULATED EVENTS
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

    if not generated_events:
        raise HTTPException(
            status_code=400,
            detail="The simulation generated no events.",
        )

    # ==========================================================
    # CONVERT GENERATED EVENTS TO DATABASE EVENTS
    # ==========================================================

    database_events: list[Event] = []

    try:
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

        # Make sure the generated Event rows are sent to the
        # database before the analytics processor reads them.
        db.flush()

        # ======================================================
        # PROCESS COMPLETE COGNIFLOW ANALYTICS PIPELINE
        # ======================================================

        processor = EventProcessor(db)

        analytics_results = processor.process_all_developers(
            persist=True,
        )

        # EventProcessor commits the derived analytics.

    except ValueError as exc:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to generate, persist, or process "
                "the CogniFlow simulation."
            ),
        ) from exc

    # ==========================================================
    # ANALYTICS SUMMARY
    # ==========================================================

    total_flow_sessions = sum(
        result.get("flow_sessions", 0)
        for result in analytics_results
    )

    total_interruptions = sum(
        result.get("interruptions", 0)
        for result in analytics_results
    )

    total_context_switches = sum(
        result.get("context_switches", 0)
        for result in analytics_results
    )

    total_recovery_seconds = sum(
        result.get("recovery_time_seconds", 0)
        for result in analytics_results
    )

    # ==========================================================
    # RETURN COMPLETE SIMULATION SUMMARY
    # ==========================================================

    return {
        "message": "Simulation completed.",
        "work_date": work_date.isoformat(),
        "developers": len(developers),
        "tasks": len(tasks),
        "events_generated": len(generated_events),
        "events_persisted": len(database_events),
        "analytics": {
            "developers_processed": len(analytics_results),
            "flow_sessions": total_flow_sessions,
            "interruptions": total_interruptions,
            "context_switches": total_context_switches,
            "recovery_time_seconds": total_recovery_seconds,
        },
    }