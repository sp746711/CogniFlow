"""Simulation API routes."""

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.developer import Developer
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
    """Generate one simulated CogniFlow workday.

    This uses only demo/simulated data.
    """

    if work_date is None:
        work_date = datetime.now()

    developers = list(
        db.scalars(
            select(Developer)
            .order_by(Developer.id)
        ).all()
    )

    tasks = list(
        db.scalars(
            select(Task)
            .order_by(Task.id)
        ).all()
    )

    runner = SimulationRunner(
        config=DEFAULT_CONFIG,
    )

    events = runner.run(
        work_date=work_date,
        developers=developers,
        tasks=tasks,
    )

    return {
        "message": "Simulation completed.",
        "work_date": work_date.isoformat(),
        "developers": len(developers),
        "tasks": len(tasks),
        "events_generated": len(events),
    }