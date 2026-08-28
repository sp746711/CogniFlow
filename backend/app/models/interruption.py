"""Interruption model for CogniFlow."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.developer import Developer
    from app.models.event import Event


class Interruption(Base):
    """
    Represents an activity that interrupts a developer's focused work.

    An interruption can be associated with the event that caused it.
    The actual rules for deciding whether an event is an interruption
    will be implemented later in the analytics/event-processing layer.
    """

    __tablename__ = "interruptions"

    # ==============================================================
    # PRIMARY KEY
    # ==============================================================

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    # ==============================================================
    # DEVELOPER
    # ==============================================================

    developer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "developers.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ==============================================================
    # EVENT THAT CAUSED THE INTERRUPTION
    # ==============================================================

    event_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "events.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    # ==============================================================
    # INTERRUPTION TIME
    # ==============================================================

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    # ==============================================================
    # INTERRUPTION TYPE
    # ==============================================================

    interruption_type: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )

    # Example values may later include:
    #
    # Slack
    # Jira
    # context_switch
    #
    # The final classification rules will be defined later.

    # ==============================================================
    # INTERRUPTION DURATION
    # ==============================================================

    duration_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # ==============================================================
    # DESCRIPTION
    # ==============================================================

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==============================================================
    # RELATIONSHIPS
    # ==============================================================

    developer: Mapped["Developer"] = relationship(
        "Developer",
        back_populates="interruptions",
    )

    event: Mapped["Event | None"] = relationship(
        "Event",
    )