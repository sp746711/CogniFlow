"""Unified activity event API routes."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.dependencies import get_db
from app.models.event import Event
from app.schemas.event import EventResponse

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get("", response_model=list[EventResponse])
def get_events(
    developer_id: int | None = None,
    source: str | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    db: Session = Depends(get_db),
) -> list[Event]:
    """Return simulated IDE, Slack, Jira and GitHub events."""

    statement = (
        select(Event)
        .options(
            selectinload(Event.developer),
            selectinload(Event.task),
        )
        .order_by(Event.timestamp)
    )

    if developer_id is not None:
        statement = statement.where(
            Event.developer_id == developer_id
        )

    if source is not None:
        statement = statement.where(
            Event.source == source
        )

    if start_time is not None:
        statement = statement.where(
            Event.timestamp >= start_time
        )

    if end_time is not None:
        statement = statement.where(
            Event.timestamp <= end_time
        )

    return list(db.scalars(statement).all())


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
) -> Event:
    """Return one simulated event."""

    statement = (
        select(Event)
        .options(
            selectinload(Event.developer),
            selectinload(Event.task),
        )
        .where(Event.id == event_id)
    )

    event = db.scalar(statement)

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )

    return event