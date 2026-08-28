"""Context-switch analytics API routes for CogniFlow."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.event_processor import EventProcessor


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

    If developer_id is provided, only that developer is processed.
    Otherwise, all developers are processed.

    EventProcessor is used as the central analytics pipeline so that
    context-switch results remain consistent with flow,
    interruptions, recovery, and flow-score calculations.
    """

    processor = EventProcessor(db)

    # ==========================================================
    # SINGLE DEVELOPER
    # ==========================================================

    if developer_id is not None:
        try:
            result = processor.process_developer(
                developer_id=developer_id,
                persist=True,
            )

        except ValueError as exc:
            raise HTTPException(
                status_code=404,
                detail=str(exc),
            ) from exc

        return {
            "developer_id": developer_id,
            "events_analyzed": result["event_count"],
            "context_switches": result["context_switches"],
            "message": "Context-switch analysis completed.",
        }

    # ==========================================================
    # ALL DEVELOPERS
    # ==========================================================

    try:
        results = processor.process_all_developers(
            persist=True,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "developer_count": len(results),
        "developers": [
            {
                "developer_id": result["developer_id"],
                "events_analyzed": result["event_count"],
                "context_switches": result["context_switches"],
            }
            for result in results
        ],
        "message": "Context-switch analysis completed.",
    }