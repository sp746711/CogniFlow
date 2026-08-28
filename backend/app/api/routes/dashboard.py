"""Dashboard API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("")
def get_dashboard(
    db: Session = Depends(get_db),
) -> dict:
    """Return the complete dynamic dashboard dataset."""

    service = DashboardService(db)

    return service.get_dashboard()


@router.get("/developer/{developer_id}")
def get_developer_dashboard(
    developer_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """Return dashboard metrics for one developer."""

    service = DashboardService(db)

    return service.get_developer_dashboard(
        developer_id
    )