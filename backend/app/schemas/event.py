"""Pydantic schemas for unified CogniFlow activity events."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EventBase(BaseModel):
    """Common event fields."""

    developer_id: int
    team_id: int
    task_id: int | None = None

    timestamp: datetime

    source: str = Field(
        ...,
        min_length=1,
        max_length=30,
    )

    event_type: str = Field(
        ...,
        min_length=1,
        max_length=60,
    )

    context: str = Field(
        ...,
        min_length=1,
        max_length=30,
    )

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
    )

    description: str | None = None

    related_developer_id: int | None = None

    event_metadata: dict[str, Any] | None = None


class EventCreate(EventBase):
    """Schema used to create a simulated activity event."""

    pass


class EventResponse(EventBase):
    """Full event API response."""

    model_config = ConfigDict(from_attributes=True)

    id: int


class EventTimelineItem(BaseModel):
    """
    Compact event representation for the unified developer timeline.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    source: str
    event_type: str
    context: str
    title: str
    developer_id: int
    team_id: int
    task_id: int | None = None