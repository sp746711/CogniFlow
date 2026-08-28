"""Event processing service for CogniFlow.

This service coordinates the analytics pipeline:

Events
    -> context switches
    -> interruptions
    -> flow sessions
    -> recovery
    -> flow score
    -> persisted metrics

The project uses simulated IDE, Slack, Jira and GitHub events only.
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.context_switch import ContextSwitch
from app.models.developer import Developer
from app.models.event import Event
from app.models.flow_session import FlowSession
from app.models.interruption import Interruption
from app.models.metric import Metric
from app.services.context_switch_analyzer import ContextSwitchAnalyzer
from app.services.flow_analyzer import FlowAnalyzer
from app.services.interruption_analyzer import InterruptionAnalyzer
from app.services.recovery_analyzer import RecoveryAnalyzer
from app.services.score_calculator import FlowScoreCalculator


class EventProcessor:
    """Coordinate processing of a developer's unified event timeline."""

    def __init__(
        self,
        session: Session,
        *,
        flow_analyzer: FlowAnalyzer | None = None,
        interruption_analyzer: InterruptionAnalyzer | None = None,
        context_switch_analyzer: ContextSwitchAnalyzer | None = None,
        recovery_analyzer: RecoveryAnalyzer | None = None,
        score_calculator: FlowScoreCalculator | None = None,
    ) -> None:
        self.session = session
        self.flow_analyzer = flow_analyzer or FlowAnalyzer()
        self.interruption_analyzer = (
            interruption_analyzer or InterruptionAnalyzer()
        )
        self.context_switch_analyzer = (
            context_switch_analyzer or ContextSwitchAnalyzer()
        )
        self.recovery_analyzer = recovery_analyzer or RecoveryAnalyzer()
        self.score_calculator = score_calculator or FlowScoreCalculator()

    def get_events(
        self,
        developer_id: int,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[Event]:
        """Return a developer's events in chronological order."""

        statement = (
            select(Event)
            .where(Event.developer_id == developer_id)
            .order_by(Event.timestamp.asc(), Event.id.asc())
        )

        if start_time is not None:
            statement = statement.where(Event.timestamp >= start_time)

        if end_time is not None:
            statement = statement.where(Event.timestamp <= end_time)

        return list(self.session.scalars(statement).all())

    def process_developer(
        self,
        developer_id: int,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        persist: bool = True,
    ) -> dict:
        """Process one developer's complete unified activity timeline."""

        developer = self.session.get(Developer, developer_id)

        if developer is None:
            raise ValueError(f"Developer {developer_id} was not found.")

        events = self.get_events(
            developer_id,
            start_time=start_time,
            end_time=end_time,
        )

        if not events:
            return {
                "developer_id": developer_id,
                "event_count": 0,
                "flow_sessions": 0,
                "interruptions": 0,
                "context_switches": 0,
                "recovery_time_seconds": 0,
                "flow_score": 0.0,
            }

        flow_sessions = self.flow_analyzer.analyze(events)

        interruptions = self.interruption_analyzer.analyze(events)

        context_switches = self.context_switch_analyzer.analyze(events)

        recovery_times = self.recovery_analyzer.analyze(
            events,
            interruptions,
            context_switches,
        )

        score = self.score_calculator.calculate(
            events=events,
            flow_sessions=flow_sessions,
            interruptions=interruptions,
            context_switches=context_switches,
            recovery_times=recovery_times,
        )

        if persist:
            self._persist_analysis(
                developer_id=developer_id,
                flow_sessions=flow_sessions,
                interruptions=interruptions,
                context_switches=context_switches,
                score=score,
            )

        return {
            "developer_id": developer_id,
            "event_count": len(events),
            "flow_sessions": len(flow_sessions),
            "interruptions": len(interruptions),
            "context_switches": len(context_switches),
            "recovery_time_seconds": sum(recovery_times),
            "flow_score": score["flow_score"],
            "metrics": score,
        }

    def process_all_developers(
        self,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        persist: bool = True,
    ) -> list[dict]:
        """Process every developer with generated events."""

        developers = list(self.session.scalars(select(Developer)).all())

        results: list[dict] = []

        for developer in developers:
            result = self.process_developer(
                developer.id,
                start_time=start_time,
                end_time=end_time,
                persist=persist,
            )
            results.append(result)

        if persist:
            self.session.commit()

        return results

    def _persist_analysis(
        self,
        *,
        developer_id: int,
        flow_sessions: Iterable[dict],
        interruptions: Iterable[dict],
        context_switches: Iterable[dict],
        score: dict,
    ) -> None:
        """Persist calculated analytics for one developer.

        Existing derived analytics for the same developer are removed first.
        Raw events and source data are never removed.
        """

        self.session.execute(
            delete(FlowSession).where(
                FlowSession.developer_id == developer_id
            )
        )

        self.session.execute(
            delete(Interruption).where(
                Interruption.developer_id == developer_id
            )
        )

        self.session.execute(
            delete(ContextSwitch).where(
                ContextSwitch.developer_id == developer_id
            )
        )

        self.session.execute(
            delete(Metric).where(
                Metric.developer_id == developer_id
            )
        )

        self.session.flush()

        for item in flow_sessions:
            self.session.add(
                FlowSession(
                    developer_id=developer_id,
                    start_time=item["start_time"],
                    end_time=item.get("end_time"),
                    duration_seconds=item.get("duration_seconds"),
                    focused_event_count=item.get("focused_event_count", 0),
                    notes=item.get("notes"),
                )
            )

        for item in interruptions:
            self.session.add(
                Interruption(
                    developer_id=developer_id,
                    event_id=item.get("event_id"),
                    timestamp=item["timestamp"],
                    interruption_type=item["interruption_type"],
                    duration_seconds=item.get("duration_seconds"),
                    description=item.get("description"),
                )
            )

        for item in context_switches:
            self.session.add(
                ContextSwitch(
                    developer_id=developer_id,
                    from_context=item["from_context"],
                    to_context=item["to_context"],
                    timestamp=item["timestamp"],
                    from_event_id=item.get("from_event_id"),
                    to_event_id=item.get("to_event_id"),
                    duration_seconds=item.get("duration_seconds"),
                )
            )

        calculated_at = datetime.now().astimezone()

        metrics = {
            "total_events": float(score["total_events"]),
            "focused_time_seconds": float(score["focused_time_seconds"]),
            "flow_session_count": float(score["flow_session_count"]),
            "average_flow_seconds": float(score["average_flow_seconds"]),
            "interruption_count": float(score["interruption_count"]),
            "context_switch_count": float(score["context_switch_count"]),
            "recovery_time_seconds": float(score["recovery_time_seconds"]),
            "flow_score": float(score["flow_score"]),
        }

        for metric_name, value in metrics.items():
            self.session.add(
                Metric(
                    developer_id=developer_id,
                    metric_name=metric_name,
                    scope="developer",
                    value=value,
                    calculated_at=calculated_at,
                    description=(
                        f"Calculated CogniFlow metric: {metric_name}."
                    ),
                )
            )

        self.session.flush()