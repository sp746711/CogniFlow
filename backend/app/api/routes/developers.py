"""Developer API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.dependencies import get_db
from app.models.developer import Developer
from app.schemas.developer import DeveloperResponse

router = APIRouter(
    prefix="/developers",
    tags=["Developers"],
)


@router.get("", response_model=list[DeveloperResponse])
def get_developers(
    db: Session = Depends(get_db),
) -> list[Developer]:
    """Return all 25 simulated developers."""

    statement = (
        select(Developer)
        .options(selectinload(Developer.team))
        .order_by(Developer.id)
    )

    return list(db.scalars(statement).all())


@router.get("/{developer_id}", response_model=DeveloperResponse)
def get_developer(
    developer_id: int,
    db: Session = Depends(get_db),
) -> Developer:
    """Return one developer."""

    statement = (
        select(Developer)
        .options(selectinload(Developer.team))
        .where(Developer.id == developer_id)
    )

    developer = db.scalar(statement)

    if developer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Developer not found.",
        )

    return developer