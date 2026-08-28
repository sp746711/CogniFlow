"""Simulated Jira task and bug model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.team import Team
    from app.models.developer import Developer
    from app.models.event import Event


# A single Jira task or bug can involve multiple developers.
#
# Example:
#
# BUG-102
#   ├── DEV003 → investigates
#   └── DEV005 → implements
#
# This many-to-many table connects tasks with all developers
# participating in that task.
task_developers = Table(
    "task_developers",
    Base.metadata,
    Column(
        "task_id",
        ForeignKey(
            "tasks.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    Column(
        "developer_id",
        ForeignKey(
            "developers.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
)


class Task(Base):
    """Represents one simulated Jira task or bug."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    task_key: Mapped[str] = mapped_column(
        String(40),
        unique=True,
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    issue_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        index=True,
    )

    priority: Mapped[str | None] = mapped_column(
        String(30),
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
        back_populates="tasks",
    )

    developers: Mapped[list["Developer"]] = relationship(
        "Developer",
        secondary=task_developers,
        back_populates="tasks",
    )

    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="task",
    )