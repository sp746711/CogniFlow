"""Interruption analytics API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.interruption_analyzer import InterruptionAnalyzer

router = APIRouter(
    prefix="/interruptions",
    tags=["Interruptions"],
)


@router.get("")
def get_interruptions(
    developer_id: int | None = None,
    db: Session = Depends(get_db),
) -> dict:
    """Return interruption analytics."""

    analyzer = InterruptionAnalyzer(db)

    if developer_id is not None:
        return analyzer.analyze_developer(developer_id)

    return analyzer.analyze_all()