"""Reporting API routes."""

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/daily")
def get_daily_report(
    work_date: datetime | None = None,
    db: Session = Depends(get_db),
) -> dict:
    """Return a simulated daily productivity report."""

    if work_date is None:
        work_date = datetime.now()

    service = DashboardService(db)

    return service.get_daily_report(
        work_date=work_date
    )