"""Dashboard analytics service for CogniFlow."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.context_switch import ContextSwitch
from app.models.developer import Developer
from app.models.event import Event
from app.models.flow_session import FlowSession
from app.models.interruption import Interruption
from app.models.metric import Metric
from app.models.team import Team


class DashboardService:
    """Provide dynamic dashboard data from PostgreSQL."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_overview(
        self,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> dict[str, Any]:
        """Return dynamic dashboard overview metrics."""

        developer_count = self._count_developers()
        team_count = self._count_teams()
        event_count = self._count_events(
            start_time=start_time,
            end_time=end_time,
        )
        flow_session_count = self._count_flow_sessions(
            start_time=start_time,
            end_time=end_time,
        )
        interruption_count = self._count_interruptions(
            start_time=start_time,
            end_time=end_time,
        )
        context_switch_count = self._count_context_switches(
            start_time=start_time,
            end_time=end_time,
        )

        total_focused_time = self._sum_flow_duration(
            start_time=start_time,
            end_time=end_time,
        )

        average_flow = self._average_flow_duration(
            start_time=start_time,
            end_time=end_time,
        )

        total_recovery_time = self._sum_recovery_time(
            start_time=start_time,
            end_time=end_time,
        )

        flow_score = self._average_metric(
            metric_name="flow_score",
            start_time=start_time,
            end_time=end_time,
        )

        return {
            "teams": team_count,
            "developers": developer_count,
            "events": event_count,
            "flow_sessions": flow_session_count,
            "total_focused_time_seconds": total_focused_time,
            "average_flow_seconds": round(
                average_flow,
                2,
            ),
            "interruptions": interruption_count,
            "context_switches": context_switch_count,
            "recovery_time_seconds": total_recovery_time,
            "flow_score": round(
                flow_score,
                2,
            ),
        }

    def get_developer_summary(
        self,
        developer_id: int,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> dict[str, Any]:
        """Return analytics for one developer."""

        developer = self.session.get(
            Developer,
            developer_id,
        )

        if developer is None:
            raise ValueError(
                f"Developer {developer_id} was not found."
            )

        events = self._count_events(
            developer_id=developer_id,
            start_time=start_time,
            end_time=end_time,
        )

        flow_sessions = self._count_flow_sessions(
            developer_id=developer_id,
            start_time=start_time,
            end_time=end_time,
        )

        focused_time = self._sum_flow_duration(
            developer_id=developer_id,
            start_time=start_time,
            end_time=end_time,
        )

        interruptions = self._count_interruptions(
            developer_id=developer_id,
            start_time=start_time,
            end_time=end_time,
        )

        context_switches = self._count_context_switches(
            developer_id=developer_id,
            start_time=start_time,
            end_time=end_time,
        )

        recovery_time = self._sum_recovery_time(
            developer_id=developer_id,
            start_time=start_time,
            end_time=end_time,
        )

        flow_score = self._latest_metric(
            developer_id=developer_id,
            metric_name="flow_score",
        )

        average_flow = self._average_flow_duration(
            developer_id=developer_id,
            start_time=start_time,
            end_time=end_time,
        )

        return {
            "developer_id": developer.id,
            "developer_code": developer.developer_code,
            "name": developer.name,
            "role": developer.role,
            "behavior_profile": developer.behavior_profile,
            "team_id": developer.team_id,
            "events": events,
            "flow_sessions": flow_sessions,
            "focused_time_seconds": focused_time,
            "average_flow_seconds": round(
                average_flow,
                2,
            ),
            "interruptions": interruptions,
            "context_switches": context_switches,
            "recovery_time_seconds": recovery_time,
            "flow_score": round(
                flow_score,
                2,
            ),
        }

    def get_developer_rankings(
        self,
        *,
        limit: int = 25,
    ) -> list[dict[str, Any]]:
        """Return developers ordered by flow score."""

        safe_limit = max(
            1,
            min(limit, 100),
        )

        developers = list(
            self.session.scalars(
                select(Developer).order_by(
                    Developer.developer_code.asc()
                )
            ).all()
        )

        rankings: list[dict[str, Any]] = []

        for developer in developers:
            score = self._latest_metric(
                developer_id=developer.id,
                metric_name="flow_score",
            )

            rankings.append(
                {
                    "developer_id": developer.id,
                    "developer_code": developer.developer_code,
                    "name": developer.name,
                    "team_id": developer.team_id,
                    "flow_score": round(score, 2),
                }
            )

        rankings.sort(
            key=lambda item: item["flow_score"],
            reverse=True,
        )

        return rankings[:safe_limit]

    def get_team_summary(
        self,
        team_id: int,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> dict[str, Any]:
        """Return dynamic analytics for a team."""

        team = self.session.get(
            Team,
            team_id,
        )

        if team is None:
            raise ValueError(
                f"Team {team_id} was not found."
            )

        developer_ids = list(
            self.session.scalars(
                select(Developer.id).where(
                    Developer.team_id == team_id
                )
            ).all()
        )

        if not developer_ids:
            return {
                "team_id": team.id,
                "team_name": team.name,
                "developers": 0,
                "events": 0,
                "flow_sessions": 0,
                "focused_time_seconds": 0,
                "interruptions": 0,
                "context_switches": 0,
                "recovery_time_seconds": 0,
                "flow_score": 0.0,
            }

        return {
            "team_id": team.id,
            "team_name": team.name,
            "developers": len(developer_ids),
            "events": self._count_events(
                developer_ids=developer_ids,
                start_time=start_time,
                end_time=end_time,
            ),
            "flow_sessions": self._count_flow_sessions(
                developer_ids=developer_ids,
                start_time=start_time,
                end_time=end_time,
            ),
            "focused_time_seconds": self._sum_flow_duration(
                developer_ids=developer_ids,
                start_time=start_time,
                end_time=end_time,
            ),
            "interruptions": self._count_interruptions(
                developer_ids=developer_ids,
                start_time=start_time,
                end_time=end_time,
            ),
            "context_switches": self._count_context_switches(
                developer_ids=developer_ids,
                start_time=start_time,
                end_time=end_time,
            ),
            "recovery_time_seconds": self._sum_recovery_time(
                developer_ids=developer_ids,
                start_time=start_time,
                end_time=end_time,
            ),
            "flow_score": round(
                self._average_metric_for_developers(
                    developer_ids,
                    "flow_score",
                ),
                2,
            ),
        }

    def get_daily_report(
        self,
        *,
        work_date: datetime,
    ) -> dict[str, Any]:
        """Return a dynamic daily productivity report."""

        start_time = work_date.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        end_time = work_date.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999,
        )

        overview = self.get_overview(
            start_time=start_time,
            end_time=end_time,
        )

        return {
            "work_date": start_time.date().isoformat(),
            "teams": overview["teams"],
            "developers": overview["developers"],
            "events": overview["events"],
            "flow_sessions": overview["flow_sessions"],
            "total_focused_time_seconds": overview[
                "total_focused_time_seconds"
            ],
            "average_flow_seconds": overview["average_flow_seconds"],
            "interruptions": overview["interruptions"],
            "context_switches": overview["context_switches"],
            "recovery_time_seconds": overview[
                "recovery_time_seconds"
            ],
            "flow_score": overview["flow_score"],
        }

    def get_recent_events(
        self,
        *,
        limit: int = 50,
    ) -> list[Event]:
        """Return the latest simulated activity events."""

        safe_limit = max(
            1,
            min(limit, 500),
        )

        statement = (
            select(Event)
            .order_by(
                Event.timestamp.desc(),
                Event.id.desc(),
            )
            .limit(safe_limit)
        )

        return list(
            self.session.scalars(statement).all()
        )

    def get_activity_timeline(
        self,
        developer_id: int,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[dict[str, Any]]:
        """Return one chronological unified timeline."""

        statement = (
            select(Event)
            .where(Event.developer_id == developer_id)
            .order_by(
                Event.timestamp.asc(),
                Event.id.asc(),
            )
        )

        if start_time is not None:
            statement = statement.where(
                Event.timestamp >= start_time
            )

        if end_time is not None:
            statement = statement.where(
                Event.timestamp <= end_time
            )

        events = list(
            self.session.scalars(statement).all()
        )

        return [
            {
                "id": event.id,
                "developer_id": event.developer_id,
                "team_id": event.team_id,
                "task_id": event.task_id,
                "timestamp": event.timestamp,
                "source": event.source,
                "event_type": event.event_type,
                "context": event.context,
                "title": event.title,
                "description": event.description,
                "related_developer_id": (
                    event.related_developer_id
                ),
                "metadata": event.event_metadata,
            }
            for event in events
        ]

    def _count_developers(self) -> int:
        return int(
            self.session.scalar(
                select(func.count(Developer.id))
            )
            or 0
        )

    def _count_teams(self) -> int:
        return int(
            self.session.scalar(
                select(func.count(Team.id))
            )
            or 0
        )

    def _count_events(
        self,
        *,
        developer_id: int | None = None,
        developer_ids: list[int] | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> int:
        statement = select(
            func.count(Event.id)
        )

        if developer_id is not None:
            statement = statement.where(
                Event.developer_id == developer_id
            )

        if developer_ids is not None:
            statement = statement.where(
                Event.developer_id.in_(developer_ids)
            )

        if start_time is not None:
            statement = statement.where(
                Event.timestamp >= start_time
            )

        if end_time is not None:
            statement = statement.where(
                Event.timestamp <= end_time
            )

        return int(
            self.session.scalar(statement)
            or 0
        )

    def _count_flow_sessions(
        self,
        *,
        developer_id: int | None = None,
        developer_ids: list[int] | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> int:
        statement = select(
            func.count(FlowSession.id)
        )

        if developer_id is not None:
            statement = statement.where(
                FlowSession.developer_id == developer_id
            )

        if developer_ids is not None:
            statement = statement.where(
                FlowSession.developer_id.in_(developer_ids)
            )

        if start_time is not None:
            statement = statement.where(
                FlowSession.start_time >= start_time
            )

        if end_time is not None:
            statement = statement.where(
                FlowSession.start_time <= end_time
            )

        return int(
            self.session.scalar(statement)
            or 0
        )

    def _sum_flow_duration(
        self,
        *,
        developer_id: int | None = None,
        developer_ids: list[int] | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> int:
        statement = select(
            func.coalesce(
                func.sum(
                    FlowSession.duration_seconds
                ),
                0,
            )
        )

        if developer_id is not None:
            statement = statement.where(
                FlowSession.developer_id == developer_id
            )

        if developer_ids is not None:
            statement = statement.where(
                FlowSession.developer_id.in_(developer_ids)
            )

        if start_time is not None:
            statement = statement.where(
                FlowSession.start_time >= start_time
            )

        if end_time is not None:
            statement = statement.where(
                FlowSession.start_time <= end_time
            )

        return int(
            self.session.scalar(statement)
            or 0
        )

    def _average_flow_duration(
        self,
        *,
        developer_id: int | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> float:
        statement = select(
            func.avg(
                FlowSession.duration_seconds
            )
        )

        if developer_id is not None:
            statement = statement.where(
                FlowSession.developer_id == developer_id
            )

        if start_time is not None:
            statement = statement.where(
                FlowSession.start_time >= start_time
            )

        if end_time is not None:
            statement = statement.where(
                FlowSession.start_time <= end_time
            )

        return float(
            self.session.scalar(statement)
            or 0.0
        )

    def _count_interruptions(
        self,
        *,
        developer_id: int | None = None,
        developer_ids: list[int] | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> int:
        statement = select(
            func.count(Interruption.id)
        )

        if developer_id is not None:
            statement = statement.where(
                Interruption.developer_id == developer_id
            )

        if developer_ids is not None:
            statement = statement.where(
                Interruption.developer_id.in_(developer_ids)
            )

        if start_time is not None:
            statement = statement.where(
                Interruption.timestamp >= start_time
            )

        if end_time is not None:
            statement = statement.where(
                Interruption.timestamp <= end_time
            )

        return int(
            self.session.scalar(statement)
            or 0
        )

    def _count_context_switches(
        self,
        *,
        developer_id: int | None = None,
        developer_ids: list[int] | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> int:
        statement = select(
            func.count(ContextSwitch.id)
        )

        if developer_id is not None:
            statement = statement.where(
                ContextSwitch.developer_id == developer_id
            )

        if developer_ids is not None:
            statement = statement.where(
                ContextSwitch.developer_id.in_(developer_ids)
            )

        if start_time is not None:
            statement = statement.where(
                ContextSwitch.timestamp >= start_time
            )

        if end_time is not None:
            statement = statement.where(
                ContextSwitch.timestamp <= end_time
            )

        return int(
            self.session.scalar(statement)
            or 0
        )

    def _sum_recovery_time(
        self,
        *,
        developer_id: int | None = None,
        developer_ids: list[int] | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> int:
        """Return persisted recovery-time metrics."""

        statement = select(
            func.coalesce(
                func.sum(Metric.value),
                0,
            )
        ).where(
            Metric.metric_name == "recovery_time_seconds"
        )

        if developer_id is not None:
            statement = statement.where(
                Metric.developer_id == developer_id
            )

        if developer_ids is not None:
            statement = statement.where(
                Metric.developer_id.in_(developer_ids)
            )

        if start_time is not None:
            statement = statement.where(
                Metric.calculated_at >= start_time
            )

        if end_time is not None:
            statement = statement.where(
                Metric.calculated_at <= end_time
            )

        return int(
            self.session.scalar(statement)
            or 0
        )

    def _average_metric(
        self,
        *,
        metric_name: str,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> float:
        statement = select(
            func.avg(Metric.value)
        ).where(
            Metric.metric_name == metric_name
        )

        if start_time is not None:
            statement = statement.where(
                Metric.calculated_at >= start_time
            )

        if end_time is not None:
            statement = statement.where(
                Metric.calculated_at <= end_time
            )

        return float(
            self.session.scalar(statement)
            or 0.0
        )

    def _latest_metric(
        self,
        *,
        developer_id: int,
        metric_name: str,
    ) -> float:
        statement = (
            select(Metric.value)
            .where(
                Metric.developer_id == developer_id,
                Metric.metric_name == metric_name,
            )
            .order_by(
                Metric.calculated_at.desc(),
                Metric.id.desc(),
            )
            .limit(1)
        )

        return float(
            self.session.scalar(statement)
            or 0.0
        )

    def _average_metric_for_developers(
        self,
        developer_ids: list[int],
        metric_name: str,
    ) -> float:
        if not developer_ids:
            return 0.0

        statement = select(
            func.avg(Metric.value)
        ).where(
            Metric.developer_id.in_(developer_ids),
            Metric.metric_name == metric_name,
        )

        return float(
            self.session.scalar(statement)
            or 0.0
        )