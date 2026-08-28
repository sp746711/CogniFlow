"""Flow analytics API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.flow_analyzer import FlowAnalyzer

router = APIRouter(
    prefix="/flow",
    tags=["Flow"],
)


@router.get("")
def get_flow_metrics(
    developer_id: int | None = None,
    db: Session = Depends(get_db),
) -> dict:
    """Return flow analytics for the simulated workforce."""

    analyzer = FlowAnalyzer(db)

    if developer_id is not None:
        return analyzer.analyze_developer(developer_id)

    return analyzer.analyze_all()