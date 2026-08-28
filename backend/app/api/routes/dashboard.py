"""Dashboard API routes for CogniFlow."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.developer import Developer
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("")
def get_dashboard(
    db: Session = Depends(get_db),
) -> dict:
    """
    Return the complete dynamic CogniFlow dashboard dataset.

    DashboardService is responsible for combining developer,
    activity, and analytics data for the dashboard.
    """

    service = DashboardService(db)

    try:
        return service.get_overview()

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get("/developer/{developer_id}")
def get_developer_dashboard(
    developer_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """
    Return the dashboard dataset for one developer.
    """

    # ==========================================================
    # VALIDATE DEVELOPER
    # ==========================================================

    developer = db.scalar(
        select(Developer).where(
            Developer.id == developer_id
        )
    )

    if developer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Developer {developer_id} not found.",
        )

    # ==========================================================
    # GENERATE DEVELOPER DASHBOARD
    # ==========================================================

    service = DashboardService(db)

    try:
        return service.get_developer_summary(
            developer_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc