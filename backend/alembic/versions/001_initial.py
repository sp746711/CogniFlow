"""Create initial CogniFlow database schema.

Revision ID: 001_initial
Revises:
Create Date: 2026-08-28
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ---------------------------------------------------------------
# Revision identifiers
# ---------------------------------------------------------------

revision: str = "001_initial"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ---------------------------------------------------------------
# Upgrade
# ---------------------------------------------------------------


def upgrade() -> None:
    """Create the complete initial CogniFlow schema."""

    # ===========================================================
    # TEAMS
    # ===========================================================

    op.create_table(
        "teams",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "code",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_teams_name",
        "teams",
        ["name"],
        unique=False,
    )

    op.create_index(
        "ix_teams_code",
        "teams",
        ["code"],
        unique=False,
    )

    op.create_unique_constraint(
        "uq_teams_name",
        "teams",
        ["name"],
    )

    op.create_unique_constraint(
        "uq_teams_code",
        "teams",
        ["code"],
    )

    # ===========================================================
    # DEVELOPERS
    # ===========================================================

    op.create_table(
        "developers",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "developer_code",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=120),
            nullable=False,
        ),
        sa.Column(
            "role",
            sa.String(length=80),
            nullable=False,
        ),
        sa.Column(
            "behavior_profile",
            sa.String(length=80),
            nullable=False,
        ),
        sa.Column(
            "profile_description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "team_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
            ondelete="RESTRICT",
        ),
    )

    op.create_index(
        "ix_developers_developer_code",
        "developers",
        ["developer_code"],
        unique=True,
    )

    op.create_index(
        "ix_developers_team_id",
        "developers",
        ["team_id"],
        unique=False,
    )

    # ===========================================================
    # TASKS
    # ===========================================================

    op.create_table(
        "tasks",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "task_key",
            sa.String(length=40),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=200),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(length=1000),
            nullable=True,
        ),
        sa.Column(
            "issue_type",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=40),
            nullable=False,
        ),
        sa.Column(
            "priority",
            sa.String(length=30),
            nullable=True,
        ),
        sa.Column(
            "team_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
            ondelete="RESTRICT",
        ),
    )

    op.create_index(
        "ix_tasks_task_key",
        "tasks",
        ["task_key"],
        unique=True,
    )

    op.create_index(
        "ix_tasks_issue_type",
        "tasks",
        ["issue_type"],
        unique=False,
    )

    op.create_index(
        "ix_tasks_status",
        "tasks",
        ["status"],
        unique=False,
    )

    op.create_index(
        "ix_tasks_team_id",
        "tasks",
        ["team_id"],
        unique=False,
    )

    # ===========================================================
    # TASK <-> DEVELOPER
    # ===========================================================

    op.create_table(
        "task_developers",
        sa.Column(
            "task_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "developer_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["developer_id"],
            ["developers.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "task_id",
            "developer_id",
        ),
    )

    # ===========================================================
    # EVENTS
    # ===========================================================

    op.create_table(
        "events",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "developer_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "team_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "task_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "source",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "event_type",
            sa.String(length=60),
            nullable=False,
        ),
        sa.Column(
            "context",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=200),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "related_developer_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "event_metadata",
            sa.JSON(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["developer_id"],
            ["developers.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["related_developer_id"],
            ["developers.id"],
            ondelete="SET NULL",
        ),
    )

    op.create_index(
        "ix_events_developer_id",
        "events",
        ["developer_id"],
        unique=False,
    )

    op.create_index(
        "ix_events_team_id",
        "events",
        ["team_id"],
        unique=False,
    )

    op.create_index(
        "ix_events_task_id",
        "events",
        ["task_id"],
        unique=False,
    )

    op.create_index(
        "ix_events_timestamp",
        "events",
        ["timestamp"],
        unique=False,
    )

    op.create_index(
        "ix_events_source",
        "events",
        ["source"],
        unique=False,
    )

    op.create_index(
        "ix_events_event_type",
        "events",
        ["event_type"],
        unique=False,
    )

    op.create_index(
        "ix_events_context",
        "events",
        ["context"],
        unique=False,
    )

    op.create_index(
        "ix_events_related_developer_id",
        "events",
        ["related_developer_id"],
        unique=False,
    )

    op.create_index(
        "ix_events_developer_timestamp",
        "events",
        ["developer_id", "timestamp"],
        unique=False,
    )

    op.create_index(
        "ix_events_source_timestamp",
        "events",
        ["source", "timestamp"],
        unique=False,
    )

    # ===========================================================
    # FLOW SESSIONS
    # ===========================================================

    op.create_table(
        "flow_sessions",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "developer_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "start_time",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "end_time",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "duration_seconds",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "focused_event_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["developer_id"],
            ["developers.id"],
            ondelete="CASCADE",
        ),
    )

    op.create_index(
        "ix_flow_sessions_developer_id",
        "flow_sessions",
        ["developer_id"],
        unique=False,
    )

    op.create_index(
        "ix_flow_sessions_start_time",
        "flow_sessions",
        ["start_time"],
        unique=False,
    )

    # ===========================================================
    # INTERRUPTIONS
    # ===========================================================

    op.create_table(
        "interruptions",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "developer_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "event_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "interruption_type",
            sa.String(length=60),
            nullable=False,
        ),
        sa.Column(
            "duration_seconds",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["developer_id"],
            ["developers.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
            ondelete="SET NULL",
        ),
    )

    op.create_index(
        "ix_interruptions_developer_id",
        "interruptions",
        ["developer_id"],
        unique=False,
    )

    op.create_index(
        "ix_interruptions_event_id",
        "interruptions",
        ["event_id"],
        unique=False,
    )

    op.create_index(
        "ix_interruptions_timestamp",
        "interruptions",
        ["timestamp"],
        unique=False,
    )

    # ===========================================================
    # CONTEXT SWITCHES
    # ===========================================================

    op.create_table(
        "context_switches",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "developer_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "from_context",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "to_context",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "from_event_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "to_event_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "duration_seconds",
            sa.Integer(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["developer_id"],
            ["developers.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["from_event_id"],
            ["events.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["to_event_id"],
            ["events.id"],
            ondelete="SET NULL",
        ),
    )

    op.create_index(
        "ix_context_switches_developer_id",
        "context_switches",
        ["developer_id"],
        unique=False,
    )

    op.create_index(
        "ix_context_switches_from_context",
        "context_switches",
        ["from_context"],
        unique=False,
    )

    op.create_index(
        "ix_context_switches_to_context",
        "context_switches",
        ["to_context"],
        unique=False,
    )

    op.create_index(
        "ix_context_switches_timestamp",
        "context_switches",
        ["timestamp"],
        unique=False,
    )

    # ===========================================================
    # METRICS
    # ===========================================================

    op.create_table(
        "metrics",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "developer_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "metric_name",
            sa.String(length=80),
            nullable=False,
        ),
        sa.Column(
            "scope",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "value",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "calculated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "period_start",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "period_end",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["developer_id"],
            ["developers.id"],
            ondelete="CASCADE",
        ),
    )

    op.create_index(
        "ix_metrics_developer_id",
        "metrics",
        ["developer_id"],
        unique=False,
    )

    op.create_index(
        "ix_metrics_metric_name",
        "metrics",
        ["metric_name"],
        unique=False,
    )

    op.create_index(
        "ix_metrics_scope",
        "metrics",
        ["scope"],
        unique=False,
    )

    op.create_index(
        "ix_metrics_calculated_at",
        "metrics",
        ["calculated_at"],
        unique=False,
    )


# ---------------------------------------------------------------
# Downgrade
# ---------------------------------------------------------------


def downgrade() -> None:
    """Remove the complete CogniFlow database schema."""

    # Remove tables in reverse dependency order.

    op.drop_index(
        "ix_metrics_calculated_at",
        table_name="metrics",
    )
    op.drop_index(
        "ix_metrics_scope",
        table_name="metrics",
    )
    op.drop_index(
        "ix_metrics_metric_name",
        table_name="metrics",
    )
    op.drop_index(
        "ix_metrics_developer_id",
        table_name="metrics",
    )
    op.drop_table("metrics")

    op.drop_index(
        "ix_context_switches_timestamp",
        table_name="context_switches",
    )
    op.drop_index(
        "ix_context_switches_to_context",
        table_name="context_switches",
    )
    op.drop_index(
        "ix_context_switches_from_context",
        table_name="context_switches",
    )
    op.drop_index(
        "ix_context_switches_developer_id",
        table_name="context_switches",
    )
    op.drop_table("context_switches")

    op.drop_index(
        "ix_interruptions_timestamp",
        table_name="interruptions",
    )
    op.drop_index(
        "ix_interruptions_event_id",
        table_name="interruptions",
    )
    op.drop_index(
        "ix_interruptions_developer_id",
        table_name="interruptions",
    )
    op.drop_table("interruptions")

    op.drop_index(
        "ix_flow_sessions_start_time",
        table_name="flow_sessions",
    )
    op.drop_index(
        "ix_flow_sessions_developer_id",
        table_name="flow_sessions",
    )
    op.drop_table("flow_sessions")

    op.drop_index(
        "ix_events_source_timestamp",
        table_name="events",
    )
    op.drop_index(
        "ix_events_developer_timestamp",
        table_name="events",
    )
    op.drop_index(
        "ix_events_related_developer_id",
        table_name="events",
    )
    op.drop_index(
        "ix_events_context",
        table_name="events",
    )
    op.drop_index(
        "ix_events_event_type",
        table_name="events",
    )
    op.drop_index(
        "ix_events_source",
        table_name="events",
    )
    op.drop_index(
        "ix_events_timestamp",
        table_name="events",
    )
    op.drop_index(
        "ix_events_task_id",
        table_name="events",
    )
    op.drop_index(
        "ix_events_team_id",
        table_name="events",
    )
    op.drop_index(
        "ix_events_developer_id",
        table_name="events",
    )
    op.drop_table("events")

    op.drop_table("task_developers")

    op.drop_index(
        "ix_tasks_team_id",
        table_name="tasks",
    )
    op.drop_index(
        "ix_tasks_status",
        table_name="tasks",
    )
    op.drop_index(
        "ix_tasks_issue_type",
        table_name="tasks",
    )
    op.drop_index(
        "ix_tasks_task_key",
        table_name="tasks",
    )
    op.drop_table("tasks")

    op.drop_index(
        "ix_developers_team_id",
        table_name="developers",
    )
    op.drop_index(
        "ix_developers_developer_code",
        table_name="developers",
    )
    op.drop_table("developers")

    op.drop_constraint(
        "uq_teams_code",
        "teams",
        type_="unique",
    )
    op.drop_constraint(
        "uq_teams_name",
        "teams",
        type_="unique",
    )

    op.drop_index(
        "ix_teams_code",
        table_name="teams",
    )
    op.drop_index(
        "ix_teams_name",
        table_name="teams",
    )
    op.drop_table("teams")