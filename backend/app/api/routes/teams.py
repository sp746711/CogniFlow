"""Team API routes for CogniFlow."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.dependencies import get_db
from app.models.team import Team
from app.schemas.team import TeamResponse


router = APIRouter(
    prefix="/teams",
    tags=["Teams"],
)


@router.get(
    "",
    response_model=list[TeamResponse],
)
def get_teams(
    db: Session = Depends(get_db),
) -> list[Team]:
    """Return all five simulated CogniFlow teams."""

    statement = (
        select(Team)
        .options(selectinload(Team.developers))
        .order_by(Team.id)
    )

    return list(db.scalars(statement).all())


@router.get(
    "/{team_id}",
    response_model=TeamResponse,
)
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
) -> Team:
    """Return one simulated team by database ID."""

    statement = (
        select(Team)
        .options(selectinload(Team.developers))
        .where(Team.id == team_id)
    )

    team = db.scalar(statement)

    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team {team_id} not found.",
        )

    return team