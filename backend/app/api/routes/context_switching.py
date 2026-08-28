"""Context-switch analytics API routes for CogniFlow."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.developer import Developer
from app.models.event import Event
from app.services.context_switch_analyzer import ContextSwitchAnalyzer


router = APIRouter(
    prefix="/context-switching",
    tags=["Context Switching"],
)


@router.get("")
def get_context_switching(
    developer_id: int | None = None,
    db: Session = Depends(get_db),
) -> dict:
    """
    Return context-switch analytics from persisted CogniFlow events.

    If developer_id is provided, only that developer's activity is
    analyzed. Otherwise, all persisted activity is analyzed.
    """

    # ----------------------------------------------------------
    # Validate developer
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
    # Load events
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
    # Empty data
    # ----------------------------------------------------------

    if not events:
        return {
            "developer_id": developer_id,
            "events_analyzed": 0,
            "context_switches": [],
            "message": "No activity events found.",
        }

    # ----------------------------------------------------------
    # Analyze context switching
    # ----------------------------------------------------------

    analyzer = ContextSwitchAnalyzer()

    try:
        result = analyzer.analyze(events)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # ----------------------------------------------------------
    # Return result
    # ----------------------------------------------------------

    if isinstance(result, dict):
        return {
            "developer_id": developer_id,
            "events_analyzed": len(events),
            "context_switches": result,
        }

    return {
        "developer_id": developer_id,
        "events_analyzed": len(events),
        "context_switches": result,
    }