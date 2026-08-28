"""Reporting API routes for CogniFlow."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
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
    """
    Return a dynamic daily CogniFlow productivity report.

    The report is generated from persisted simulated activity.
    No real external service is contacted.
    """

    if work_date is None:
        work_date = datetime.now()

    # ==========================================================
    # VALIDATE WORK DATE
    # ==========================================================

    if work_date.year < 2000:
        raise HTTPException(
            status_code=400,
            detail="work_date must be a valid simulation date.",
        )

    # ==========================================================
    # GENERATE DAILY REPORT
    # ==========================================================

    service = DashboardService(db)

    try:
        return service.get_daily_report(
            work_date=work_date,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc