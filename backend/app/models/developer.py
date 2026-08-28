"""Developer model for the simulated CogniFlow company."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.team import Team
    from app.models.task import Task
    from app.models.event import Event
    from app.models.flow_session import FlowSession
    from app.models.interruption import Interruption
    from app.models.context_switch import ContextSwitch
    from app.models.metric import Metric


class Developer(Base):
    """Represents one virtual developer in CogniFlow."""

    __tablename__ = "developers"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    developer_code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    behavior_profile: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    profile_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey(
            "teams.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    team: Mapped["Team"] = relationship(
        "Team",
        back_populates="developers",
    )

    events: Mapped[list["Event"]] = relationship(
        "Event",
        foreign_keys="Event.developer_id",
        back_populates="developer",
        cascade="all, delete-orphan",
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        secondary="task_developers",
        back_populates="developers",
    )

    flow_sessions: Mapped[list["FlowSession"]] = relationship(
        "FlowSession",
        back_populates="developer",
        cascade="all, delete-orphan",
    )

    interruptions: Mapped[list["Interruption"]] = relationship(
        "Interruption",
        back_populates="developer",
        cascade="all, delete-orphan",
    )

    context_switches: Mapped[list["ContextSwitch"]] = relationship(
        "ContextSwitch",
        back_populates="developer",
        cascade="all, delete-orphan",
    )

    metrics: Mapped[list["Metric"]] = relationship(
        "Metric",
        back_populates="developer",
        cascade="all, delete-orphan",
    )