"""Unified activity event model for CogniFlow."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.developer import Developer
    from app.models.team import Team
    from app.models.task import Task


class Event(Base):
    """
    Represents one activity event in the unified CogniFlow timeline.

    Events can come from the four simulated activity sources:

        IDE
        Slack
        Jira
        GitHub

    The event is connected to a developer and team and can optionally
    be connected to a Jira task/bug.
    """

    __tablename__ = "events"

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
    # TEAM
    # ==============================================================

    team_id: Mapped[int] = mapped_column(
        ForeignKey(
            "teams.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    # ==============================================================
    # OPTIONAL JIRA TASK / BUG
    # ==============================================================

    task_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "tasks.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    # ==============================================================
    # TIME
    # ==============================================================

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    # ==============================================================
    # EVENT SOURCE
    # ==============================================================

    source: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    # Examples:
    #
    # IDE
    # Slack
    # Jira
    # GitHub

    # ==============================================================
    # EVENT TYPE
    # ==============================================================

    event_type: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
        index=True,
    )

    # Examples:
    #
    # IDE:
    # coding
    # debugging
    # testing
    #
    # Slack:
    # message
    # mention
    #
    # Jira:
    # task_created
    # status_changed
    # comment
    #
    # GitHub:
    # commit
    # pull_request
    # review
    # merge

    # ==============================================================
    # ACTIVITY CONTEXT
    # ==============================================================

    context: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    # Examples:
    #
    # IDE
    # SLACK
    # JIRA
    # GITHUB

    # ==============================================================
    # EVENT TITLE
    # ==============================================================

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    # ==============================================================
    # EVENT DESCRIPTION
    # ==============================================================

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==============================================================
    # RELATED DEVELOPER
    # ==============================================================

    related_developer_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "developers.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    # Example:
    #
    # DEV003 sends a Slack message to DEV005
    #
    # developer_id         = DEV003
    # related_developer_id = DEV005

    # ==============================================================
    # EXTRA EVENT DATA
    # ==============================================================

    event_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    # This allows the simulator to store source-specific information
    # without changing the database structure for every new event type.
    #
    # Example:
    #
    # {
    #     "channel": "team-1",
    #     "repository": "project-api",
    #     "commit_hash": "abc123"
    # }

    # ==============================================================
    # RELATIONSHIPS
    # ==============================================================

    developer: Mapped["Developer"] = relationship(
        "Developer",
        foreign_keys=[developer_id],
        back_populates="events",
    )

    related_developer: Mapped["Developer | None"] = relationship(
        "Developer",
        foreign_keys=[related_developer_id],
    )

    team: Mapped["Team"] = relationship(
        "Team",
        foreign_keys=[team_id],
    )

    task: Mapped["Task | None"] = relationship(
        "Task",
        back_populates="events",
    )

    # ==============================================================
    # INDEXES
    # ==============================================================

    __table_args__ = (
        Index(
            "ix_events_developer_timestamp",
            "developer_id",
            "timestamp",
        ),
        Index(
            "ix_events_source_timestamp",
            "source",
            "timestamp",
        ),
    )