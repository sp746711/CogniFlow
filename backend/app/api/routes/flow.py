"""Flow analytics API routes for CogniFlow."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.developer import Developer
from app.models.event import Event
from app.services.flow_analyzer import FlowAnalyzer


router = APIRouter(
    prefix="/flow",
    tags=["Flow"],
)


@router.get("")
def get_flow_metrics(
    developer_id: int | None = None,
    db: Session = Depends(get_db),
) -> dict:
    """
    Return flow-state analytics from persisted CogniFlow events.

    If developer_id is provided, analytics are calculated only for
    that developer. Otherwise, analytics are calculated for all
    developers represented in the event data.
    """

    # ----------------------------------------------------------
    # Validate developer when one is requested
    # ----------------------------------------------------------

    if developer_id is not None:
        developer = db.scalar(
            select(Developer).where(
                Developer.id == developer_id
            )
        )

        if developer is None:
            raise HTTPException(
                status_code=404,
                detail=f"Developer {developer_id} not found.",
            )

    # ----------------------------------------------------------
    # Load persisted events
    # ----------------------------------------------------------

    query = select(Event).order_by(Event.timestamp)

    if developer_id is not None:
        query = query.where(
            Event.developer_id == developer_id
        )

    events = list(
        db.scalars(query).all()
    )

    # ----------------------------------------------------------
    # Handle empty event data
    # ----------------------------------------------------------

    if not events:
        return {
            "developer_id": developer_id,
            "events_analyzed": 0,
            "flow": None,
            "message": "No activity events found.",
        }

    # ----------------------------------------------------------
    # Run flow analyzer
    # ----------------------------------------------------------

    analyzer = FlowAnalyzer()

    try:
        result = analyzer.analyze(events)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # ----------------------------------------------------------
    # Return analytics
    # ----------------------------------------------------------

    if isinstance(result, dict):
        return {
            "developer_id": developer_id,
            "events_analyzed": len(events),
            "flow": result,
        }

    return {
        "developer_id": developer_id,
        "events_analyzed": len(events),
        "flow": result,
    }