"""
Event processing service for CogniFlow.

This service coordinates the complete analytics pipeline:

Events
    -> context switches
    -> interruptions
    -> flow sessions
    -> recovery
    -> flow score
    -> persisted metrics

The project uses simulated IDE, Slack, Jira and GitHub events only.

Raw events are never deleted. Derived analytics are recalculated
from the current event timeline for each developer.
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
        """Initialize the central analytics processor."""

        self.session = session

        self.flow_analyzer = (
            flow_analyzer
            if flow_analyzer is not None
            else FlowAnalyzer()
        )

        self.interruption_analyzer = (
            interruption_analyzer
            if interruption_analyzer is not None
            else InterruptionAnalyzer()
        )

        self.context_switch_analyzer = (
            context_switch_analyzer
            if context_switch_analyzer is not None
            else ContextSwitchAnalyzer()
        )

        self.recovery_analyzer = (
            recovery_analyzer
            if recovery_analyzer is not None
            else RecoveryAnalyzer()
        )

        self.score_calculator = (
            score_calculator
            if score_calculator is not None
            else FlowScoreCalculator()
        )

    # ==========================================================
    # EVENT LOADING
    # ==========================================================

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

        return list(
            self.session.scalars(statement).all()
        )

    # ==========================================================
    # SINGLE DEVELOPER PROCESSING
    # ==========================================================

    def process_developer(
        self,
        developer_id: int,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        persist: bool = True,
    ) -> dict:
        """
        Process one developer's complete activity timeline.

        Pipeline:

        Events
            -> Flow
            -> Interruptions
            -> Context Switching
            -> Recovery
            -> Flow Score
            -> Persistence
        """

        developer = self.session.get(
            Developer,
            developer_id,
        )

        if developer is None:
            raise ValueError(
                f"Developer {developer_id} was not found."
            )

        events = self.get_events(
            developer_id,
            start_time=start_time,
            end_time=end_time,
        )

        # ------------------------------------------------------
        # No activity
        # ------------------------------------------------------

        if not events:
            empty_metrics = {
                "total_events": 0.0,
                "focused_time_seconds": 0.0,
                "flow_session_count": 0.0,
                "average_flow_seconds": 0.0,
                "interruption_count": 0.0,
                "context_switch_count": 0.0,
                "recovery_time_seconds": 0.0,
                "flow_score": 0.0,
            }

            if persist:
                self._clear_derived_analytics(
                    developer_id
                )
                self._persist_metrics(
                    developer_id=developer_id,
                    score=empty_metrics,
                )

            return {
                "developer_id": developer_id,
                "event_count": 0,
                "flow_sessions": 0,
                "interruptions": 0,
                "context_switches": 0,
                "recovery_time_seconds": 0.0,
                "flow_score": 0.0,
                "metrics": empty_metrics,
            }

        # ------------------------------------------------------
        # Flow analysis
        # ------------------------------------------------------

        flow_sessions = self.flow_analyzer.analyze(
            events
        )

        # ------------------------------------------------------
        # Interruption analysis
        # ------------------------------------------------------

        interruptions = (
            self.interruption_analyzer.analyze(
                events
            )
        )

        # ------------------------------------------------------
        # Context-switch analysis
        # ------------------------------------------------------

        context_switches = (
            self.context_switch_analyzer.analyze(
                events
            )
        )

        # ------------------------------------------------------
        # Recovery analysis
        # ------------------------------------------------------

        recovery_times = (
            self.recovery_analyzer.analyze(
                events,
                interruptions,
                context_switches,
            )
        )

        # ------------------------------------------------------
        # Flow score
        # ------------------------------------------------------

        score = self.score_calculator.calculate(
            events=events,
            flow_sessions=flow_sessions,
            interruptions=interruptions,
            context_switches=context_switches,
            recovery_times=recovery_times,
        )

        # ------------------------------------------------------
        # Persist derived analytics
        # ------------------------------------------------------

        if persist:
            self._persist_analysis(
                developer_id=developer_id,
                flow_sessions=flow_sessions,
                interruptions=interruptions,
                context_switches=context_switches,
                score=score,
            )

        # ------------------------------------------------------
        # Return unified result
        # ------------------------------------------------------

        return {
            "developer_id": developer_id,
            "event_count": len(events),
            "flow_sessions": len(flow_sessions),
            "interruptions": len(interruptions),
            "context_switches": len(context_switches),
            "recovery_time_seconds": sum(
                recovery_times
            ),
            "flow_score": float(
                score["flow_score"]
            ),
            "metrics": score,
        }

    # ==========================================================
    # ALL DEVELOPERS
    # ==========================================================

    def process_all_developers(
        self,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        persist: bool = True,
    ) -> list[dict]:
        """Process every developer in the database."""

        statement = (
            select(Developer)
            .order_by(Developer.id)
        )

        developers = list(
            self.session.scalars(statement).all()
        )

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

    # ==========================================================
    # PERSIST ANALYSIS
    # ==========================================================

    def _persist_analysis(
        self,
        *,
        developer_id: int,
        flow_sessions: Iterable[dict],
        interruptions: Iterable[dict],
        context_switches: Iterable[dict],
        score: dict,
    ) -> None:
        """
        Replace derived analytics for one developer.

        Raw Event records are never deleted.
        """

        self._clear_derived_analytics(
            developer_id
        )

        self.session.flush()

        # ------------------------------------------------------
        # Flow sessions
        # ------------------------------------------------------

        for item in flow_sessions:
            self.session.add(
                FlowSession(
                    developer_id=developer_id,
                    start_time=item["start_time"],
                    end_time=item.get("end_time"),
                    duration_seconds=item.get(
                        "duration_seconds"
                    ),
                    focused_event_count=item.get(
                        "focused_event_count",
                        0,
                    ),
                    notes=item.get("notes"),
                )
            )

        # ------------------------------------------------------
        # Interruptions
        # ------------------------------------------------------

        for item in interruptions:
            self.session.add(
                Interruption(
                    developer_id=developer_id,
                    event_id=item.get("event_id"),
                    timestamp=item["timestamp"],
                    interruption_type=item[
                        "interruption_type"
                    ],
                    duration_seconds=item.get(
                        "duration_seconds"
                    ),
                    description=item.get(
                        "description"
                    ),
                )
            )

        # ------------------------------------------------------
        # Context switches
        # ------------------------------------------------------

        for item in context_switches:
            self.session.add(
                ContextSwitch(
                    developer_id=developer_id,
                    from_context=item[
                        "from_context"
                    ],
                    to_context=item[
                        "to_context"
                    ],
                    timestamp=item["timestamp"],
                    from_event_id=item.get(
                        "from_event_id"
                    ),
                    to_event_id=item.get(
                        "to_event_id"
                    ),
                    duration_seconds=item.get(
                        "duration_seconds"
                    ),
                )
            )

        # ------------------------------------------------------
        # Metrics
        # ------------------------------------------------------

        self._persist_metrics(
            developer_id=developer_id,
            score=score,
        )

        self.session.flush()

    # ==========================================================
    # CLEAR DERIVED ANALYTICS
    # ==========================================================

    def _clear_derived_analytics(
        self,
        developer_id: int,
    ) -> None:
        """
        Remove previously calculated analytics.

        Only derived data is removed.
        Raw Event records remain untouched.
        """

        self.session.execute(
            delete(FlowSession).where(
                FlowSession.developer_id
                == developer_id
            )
        )

        self.session.execute(
            delete(Interruption).where(
                Interruption.developer_id
                == developer_id
            )
        )

        self.session.execute(
            delete(ContextSwitch).where(
                ContextSwitch.developer_id
                == developer_id
            )
        )

        self.session.execute(
            delete(Metric).where(
                Metric.developer_id
                == developer_id
            )
        )

    # ==========================================================
    # METRIC PERSISTENCE
    # ==========================================================

    def _persist_metrics(
        self,
        *,
        developer_id: int,
        score: dict,
    ) -> None:
        """Persist calculated developer metrics."""

        calculated_at = datetime.now().astimezone()

        metrics = {
            "total_events": float(
                score.get("total_events", 0)
            ),
            "focused_time_seconds": float(
                score.get(
                    "focused_time_seconds",
                    0,
                )
            ),
            "flow_session_count": float(
                score.get(
                    "flow_session_count",
                    0,
                )
            ),
            "average_flow_seconds": float(
                score.get(
                    "average_flow_seconds",
                    0,
                )
            ),
            "interruption_count": float(
                score.get(
                    "interruption_count",
                    0,
                )
            ),
            "context_switch_count": float(
                score.get(
                    "context_switch_count",
                    0,
                )
            ),
            "recovery_time_seconds": float(
                score.get(
                    "recovery_time_seconds",
                    0,
                )
            ),
            "flow_score": float(
                score.get(
                    "flow_score",
                    0,
                )
            ),
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
                        "Calculated CogniFlow metric: "
                        f"{metric_name}."
                    ),
                )
            )