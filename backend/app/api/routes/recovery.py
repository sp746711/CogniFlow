"""Recovery analytics API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.recovery_analyzer import RecoveryAnalyzer

router = APIRouter(
    prefix="/recovery",
    tags=["Recovery"],
)


@router.get("")
def get_recovery(
    developer_id: int | None = None,
    db: Session = Depends(get_db),
) -> dict:
    """Return recovery-time analytics."""

    analyzer = RecoveryAnalyzer(db)

    if developer_id is not None:
        return analyzer.analyze_developer(developer_id)

    return analyzer.analyze_all()