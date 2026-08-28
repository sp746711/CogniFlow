"""Pydantic schemas for simulated Jira tasks and bugs."""

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.developer import DeveloperSummary


class TaskBase(BaseModel):
    """Common Jira task fields."""

    task_key: str = Field(
        ...,
        min_length=1,
        max_length=40,
    )

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    issue_type: str = Field(
        ...,
        min_length=1,
        max_length=30,
    )

    status: str = Field(
        ...,
        min_length=1,
        max_length=40,
    )

    priority: str | None = Field(
        default=None,
        max_length=30,
    )

    team_id: int


class TaskCreate(TaskBase):
    """Schema used to create a simulated Jira task or bug."""

    developer_ids: list[int] = Field(
        default_factory=list,
    )


class TaskDeveloperSummary(BaseModel):
    """Developer participating in a Jira task."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    developer_code: str
    name: str


class TaskResponse(TaskBase):
    """Full Jira task response."""

    model_config = ConfigDict(from_attributes=True)

    id: int

    developers: list[DeveloperSummary] = Field(
        default_factory=list,
    )