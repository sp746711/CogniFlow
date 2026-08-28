"""Flow session model for CogniFlow."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.developer import Developer


class FlowSession(Base):
    """
    Represents a detected period of focused developer activity.

    A flow session belongs to one developer and records when the
    focused period started, when it ended, and how much focused
    activity occurred during that session.
    """

    __tablename__ = "flow_sessions"

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
    # SESSION TIME
    # ==============================================================

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ==============================================================
    # SESSION DURATION
    # ==============================================================

    duration_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # ==============================================================
    # FOCUSED EVENTS
    # ==============================================================

    focused_event_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # ==============================================================
    # NOTES
    # ==============================================================

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==============================================================
    # RELATIONSHIP
    # ==============================================================

    developer: Mapped["Developer"] = relationship(
        "Developer",
        back_populates="flow_sessions",
    )