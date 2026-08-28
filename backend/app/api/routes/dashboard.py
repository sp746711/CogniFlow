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

    Dashboard data is calculated from the PostgreSQL database,
    including simulated developer activity and analytics.
    """

    service = DashboardService(db)

    return service.get_dashboard()


@router.get("/developer/{developer_id}")
def get_developer_dashboard(
    developer_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """
    Return dashboard metrics for one developer.
    """

    # ----------------------------------------------------------
    # Validate developer
    # ----------------------------------------------------------

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

    # ----------------------------------------------------------
    # Generate developer dashboard
    # ----------------------------------------------------------

    service = DashboardService(db)

    return service.get_developer_dashboard(
        developer_id
    )