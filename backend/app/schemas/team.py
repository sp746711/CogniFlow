"""Pydantic schemas for teams."""

from pydantic import BaseModel, ConfigDict, Field


class TeamBase(BaseModel):
    """Common team fields."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    code: str = Field(
        ...,
        min_length=1,
        max_length=30,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )


class TeamCreate(TeamBase):
    """Schema used when creating a team."""

    pass


class TeamSummary(BaseModel):
    """Small team representation for nested responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str


class TeamResponse(TeamBase):
    """Full team response."""

    model_config = ConfigDict(from_attributes=True)

    id: int