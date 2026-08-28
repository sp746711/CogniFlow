"""Context switch model for CogniFlow."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.developer import Developer
    from app.models.event import Event


class ContextSwitch(Base):
    """
    Represents a transition from one activity context to another.

    Examples:

        IDE -> Slack
        Slack -> IDE
        IDE -> Jira
        Jira -> IDE
        IDE -> GitHub

    The actual rules for detecting and scoring context switches
    will be implemented later in the analytics layer.
    """

    __tablename__ = "context_switches"

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
    # SOURCE CONTEXT
    # ==============================================================

    from_context: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    # ==============================================================
    # DESTINATION CONTEXT
    # ==============================================================

    to_context: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    # ==============================================================
    # SWITCH TIME
    # ==============================================================

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    # ==============================================================
    # RELATED EVENTS
    # ==============================================================

    from_event_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "events.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    to_event_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "events.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    # ==============================================================
    # TIME BETWEEN ACTIVITIES
    # ==============================================================

    duration_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # ==============================================================
    # RELATIONSHIPS
    # ==============================================================

    developer: Mapped["Developer"] = relationship(
        "Developer",
        back_populates="context_switches",
    )

    from_event: Mapped["Event | None"] = relationship(
        "Event",
        foreign_keys=[from_event_id],
    )

    to_event: Mapped["Event | None"] = relationship(
        "Event",
        foreign_keys=[to_event_id],
    )