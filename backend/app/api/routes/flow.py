"""Flow analytics API routes for CogniFlow."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.developer import Developer
from app.models.event import Event
from app.models.flow_session import FlowSession
from app.models.metric import Metric


router = APIRouter(
    prefix="/flow",
    tags=["Flow"],
)


@router.get("")
def get_flow_metrics(
    developer_id: int | None = None,
    db: Session = Depends(get_db),
) -> dict:
    """
    Return persisted CogniFlow flow analytics.

    The simulation pipeline creates raw events and the
    EventProcessor calculates the derived flow analytics.

    If developer_id is provided, return flow analytics for that
    developer. Otherwise return flow analytics for all developers.
    """

    # ==========================================================
    # VALIDATE DEVELOPER
    # ==========================================================

    if developer_id is not None:
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
    # EVENT COUNT
    # ==========================================================

    event_query = select(Event)

    if developer_id is not None:
        event_query = event_query.where(
            Event.developer_id == developer_id
        )

    events = list(
        db.scalars(
            event_query.order_by(
                Event.timestamp.asc(),
                Event.id.asc(),
            )
        ).all()
    )

    # ==========================================================
    # FLOW SESSIONS
    # ==========================================================

    flow_query = select(FlowSession)

    if developer_id is not None:
        flow_query = flow_query.where(
            FlowSession.developer_id == developer_id
        )

    flow_sessions = list(
        db.scalars(
            flow_query.order_by(
                FlowSession.start_time.asc(),
                FlowSession.id.asc(),
            )
        ).all()
    )

    # ==========================================================
    # FLOW METRICS
    # ==========================================================

    metric_query = select(Metric).where(
        Metric.metric_name.in_(
            [
                "total_events",
                "focused_time_seconds",
                "flow_session_count",
                "average_flow_seconds",
                "flow_score",
            ]
        )
    )

    if developer_id is not None:
        metric_query = metric_query.where(
            Metric.developer_id == developer_id
        )

    metrics = list(
        db.scalars(
            metric_query.order_by(
                Metric.calculated_at.desc(),
                Metric.id.desc(),
            )
        ).all()
    )

    # ==========================================================
    # EMPTY STATE
    # ==========================================================

    if not events:
        return {
            "developer_id": developer_id,
            "events_analyzed": 0,
            "flow_sessions": 0,
            "flow_score": 0.0,
            "focused_time_seconds": 0.0,
            "average_flow_seconds": 0.0,
            "message": "No activity events found.",
        }

    # ==========================================================
    # USE MOST RECENT METRIC VALUE
    # ==========================================================

    metric_values: dict[str, float] = {}

    for metric in metrics:
        if metric.metric_name not in metric_values:
            metric_values[metric.metric_name] = float(
                metric.value
            )

    # ==========================================================
    # RETURN FLOW ANALYTICS
    # ==========================================================

    return {
        "developer_id": developer_id,
        "events_analyzed": len(events),
        "flow_sessions": len(flow_sessions),
        "flow_score": metric_values.get(
            "flow_score",
            0.0,
        ),
        "focused_time_seconds": metric_values.get(
            "focused_time_seconds",
            0.0,
        ),
        "average_flow_seconds": metric_values.get(
            "average_flow_seconds",
            0.0,
        ),
        "metrics": metric_values,
    }