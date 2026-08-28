"""Pydantic schemas for the CogniFlow dashboard."""

from datetime import datetime

from pydantic import BaseModel, Field


class DashboardMetric(BaseModel):
    """Single dashboard metric card."""

    name: str
    value: float
    unit: str | None = None
    description: str | None = None


class DashboardTrendPoint(BaseModel):
    """One point in a dashboard trend."""

    timestamp: datetime
    value: float


class DashboardTeamSummary(BaseModel):
    """Team information displayed on the dashboard."""

    team_id: int
    team_name: str

    developer_count: int = 0

    average_flow: float | None = None

    interruption_count: int = 0

    context_switch_count: int = 0

    recovery_time_seconds: float | None = None

    flow_score: float | None = None


class DashboardDeveloperSummary(BaseModel):
    """Developer information displayed on the dashboard."""

    developer_id: int
    developer_code: str
    developer_name: str
    team_name: str

    flow_score: float | None = None

    average_flow: float | None = None

    interruption_count: int = 0

    context_switch_count: int = 0

    recovery_time_seconds: float | None = None


class DashboardSummary(BaseModel):
    """
    Complete dashboard response.

    Values must eventually come from database events and analytics,
    not permanent hard-coded numbers.
    """

    generated_at: datetime

    working_hours_start: str = "10:00"
    working_hours_end: str = "18:00"

    total_teams: int = 0
    total_developers: int = 0
    total_events: int = 0

    average_flow: float | None = None

    total_flow_sessions: int = 0

    total_interruptions: int = 0

    total_context_switches: int = 0

    average_recovery_seconds: float | None = None

    overall_flow_score: float | None = None

    teams: list[DashboardTeamSummary] = Field(
        default_factory=list,
    )

    developers: list[DashboardDeveloperSummary] = Field(
        default_factory=list,
    )

    flow_trend: list[DashboardTrendPoint] = Field(
        default_factory=list,
    )

    interruption_trend: list[DashboardTrendPoint] = Field(
        default_factory=list,
    )

    context_switch_trend: list[DashboardTrendPoint] = Field(
        default_factory=list,
    )