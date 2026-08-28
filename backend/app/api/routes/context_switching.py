"""Context-switch analytics API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.context_switch_analyzer import ContextSwitchAnalyzer

router = APIRouter(
    prefix="/context-switching",
    tags=["Context Switching"],
)


@router.get("")
def get_context_switching(
    developer_id: int | None = None,
    db: Session = Depends(get_db),
) -> dict:
    """Return context-switch analytics."""

    analyzer = ContextSwitchAnalyzer(db)

    if developer_id is not None:
        return analyzer.analyze_developer(developer_id)

    return analyzer.analyze_all()