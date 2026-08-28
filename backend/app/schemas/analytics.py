"""Pydantic schemas for CogniFlow analytics."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FlowSessionResponse(BaseModel):
    """Flow session analytics result."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    developer_id: int

    start_time: datetime
    end_time: datetime | None = None

    duration_seconds: int | None = None

    focused_event_count: int = 0

    notes: str | None = None


class InterruptionResponse(BaseModel):
    """Detected interruption analytics result."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    developer_id: int

    event_id: int | None = None

    timestamp: datetime

    interruption_type: str

    duration_seconds: int | None = None

    description: str | None = None


class ContextSwitchResponse(BaseModel):
    """Detected context-switch analytics result."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    developer_id: int

    from_context: str
    to_context: str

    timestamp: datetime

    from_event_id: int | None = None
    to_event_id: int | None = None

    duration_seconds: int | None = None


class MetricResponse(BaseModel):
    """Calculated analytics metric."""

    model_config = ConfigDict(from_attributes=True)

    id: int

    developer_id: int | None = None

    metric_name: str
    scope: str
    value: float

    calculated_at: datetime

    period_start: datetime | None = None
    period_end: datetime | None = None

    description: str | None = None


class DeveloperAnalytics(BaseModel):
    """Analytics summary for one developer."""

    developer_id: int
    developer_code: str | None = None
    developer_name: str | None = None

    total_flow_sessions: int = 0

    average_flow: float | None = None

    total_flow_seconds: int = 0

    interruption_count: int = 0

    context_switch_count: int = 0

    average_recovery_seconds: float | None = None

    flow_score: float | None = None


class TeamAnalytics(BaseModel):
    """Analytics summary for one team."""

    team_id: int
    team_name: str | None = None

    developer_count: int = 0

    total_flow_sessions: int = 0

    average_flow: float | None = None

    total_flow_seconds: int = 0

    interruption_count: int = 0

    context_switch_count: int = 0

    average_recovery_seconds: float | None = None

    flow_score: float | None = None


class AnalyticsSummary(BaseModel):
    """Overall analytics response."""

    period_start: datetime | None = None
    period_end: datetime | None = None

    total_developers: int = 0
    total_teams: int = 0

    total_events: int = 0
    total_flow_sessions: int = 0

    average_flow: float | None = None

    total_interruptions: int = 0
    total_context_switches: int = 0

    average_recovery_seconds: float | None = None

    flow_score: float | None = None