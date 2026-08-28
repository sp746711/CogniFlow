"""Pydantic schemas for developers."""

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.team import TeamSummary


class DeveloperBase(BaseModel):
    """Common developer fields."""

    developer_code: str = Field(
        ...,
        min_length=1,
        max_length=30,
    )

    name: str = Field(
        ...,
        min_length=1,
        max_length=120,
    )

    role: str = Field(
        ...,
        min_length=1,
        max_length=80,
    )

    behavior_profile: str = Field(
        ...,
        min_length=1,
        max_length=80,
    )

    profile_description: str | None = None

    team_id: int


class DeveloperCreate(DeveloperBase):
    """Schema used when creating a simulated developer."""

    pass


class DeveloperSummary(BaseModel):
    """Small developer representation used in nested responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    developer_code: str
    name: str
    role: str


class DeveloperResponse(DeveloperBase):
    """Full developer response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    team: TeamSummary | None = None