"""Flow-score calculation for CogniFlow."""

from __future__ import annotations

from typing import Sequence

from app.models.event import Event


class FlowScoreCalculator:
    """Calculate a normalized developer flow score.

    The official project specification requires a normalized flow score,
    but does not define a mathematical formula.

    Therefore this service uses an explicit, documented implementation
    formula:

        score =
            40% focused-time ratio
            + 30% flow-session quality
            + 20% interruption quality
            + 10% recovery quality

    The result is normalized to 0-100.
    """

    FOCUSED_CONTEXT = "IDE"

    def calculate(
        self,
        *,
        events: Sequence[Event],
        flow_sessions: Sequence[dict],
        interruptions: Sequence[dict],
        context_switches: Sequence[dict],
        recovery_times: Sequence[int],
    ) -> dict:
        total_events = len(events)

        focused_events = [
            event
            for event in events
            if self._is_focused(event)
        ]

        focused_time_seconds = self._focused_time(
            flow_sessions,
        )

        total_timeline_seconds = self._timeline_seconds(events)

        focused_time_ratio = self._ratio(
            focused_time_seconds,
            total_timeline_seconds,
        )

        flow_session_quality = self._flow_session_quality(
            flow_sessions,
        )

        interruption_quality = self._interruption_quality(
            total_events,
            len(interruptions),
        )

        recovery_quality = self._recovery_quality(
            recovery_times,
        )

        flow_score = (
            focused_time_ratio * 40.0
            + flow_session_quality * 30.0
            + interruption_quality * 20.0
            + recovery_quality * 10.0
        )

        average_flow_seconds = self._average_flow(
            flow_sessions,
        )

        return {
            "total_events": total_events,
            "focused_event_count": len(focused_events),
            "focused_time_seconds": focused_time_seconds,
            "flow_session_count": len(flow_sessions),
            "average_flow_seconds": average_flow_seconds,
            "interruption_count": len(interruptions),
            "context_switch_count": len(context_switches),
            "recovery_time_seconds": sum(recovery_times),
            "average_recovery_seconds": (
                sum(recovery_times) / len(recovery_times)
                if recovery_times
                else 0.0
            ),
            "focused_time_ratio": round(
                focused_time_ratio,
                4,
            ),
            "flow_session_quality": round(
                flow_session_quality,
                4,
            ),
            "interruption_quality": round(
                interruption_quality,
                4,
            ),
            "recovery_quality": round(
                recovery_quality,
                4,
            ),
            "flow_score": round(
                self._clamp(flow_score, 0.0, 100.0),
                2,
            ),
        }

    def _focused_time(
        self,
        flow_sessions: Sequence[dict],
    ) -> int:
        return sum(
            max(
                0,
                int(session.get("duration_seconds") or 0),
            )
            for session in flow_sessions
        )

    def _timeline_seconds(
        self,
        events: Sequence[Event],
    ) -> int:
        if len(events) < 2:
            return 0

        ordered = sorted(
            events,
            key=lambda event: (event.timestamp, event.id or 0),
        )

        return max(
            0,
            int(
                (
                    ordered[-1].timestamp
                    - ordered[0].timestamp
                ).total_seconds()
            ),
        )

    def _flow_session_quality(
        self,
        flow_sessions: Sequence[dict],
    ) -> float:
        if not flow_sessions:
            return 0.0

        durations = [
            max(
                0,
                int(session.get("duration_seconds") or 0),
            )
            for session in flow_sessions
        ]

        average_duration = sum(durations) / len(durations)

        # Implementation decision:
        # 60 minutes represents a strong sustained session.
        return self._clamp(
            average_duration / (60 * 60),
            0.0,
            1.0,
        )

    def _interruption_quality(
        self,
        total_events: int,
        interruption_count: int,
    ) -> float:
        if total_events <= 0:
            return 0.0

        interruption_ratio = interruption_count / total_events

        return self._clamp(
            1.0 - interruption_ratio,
            0.0,
            1.0,
        )

    def _recovery_quality(
        self,
        recovery_times: Sequence[int],
    ) -> float:
        if not recovery_times:
            return 1.0

        average_recovery = (
            sum(recovery_times) / len(recovery_times)
        )

        # Implementation decision:
        # 30 minutes or more is treated as the maximum recovery penalty.
        return self._clamp(
            1.0 - (
                average_recovery
                / (30 * 60)
            ),
            0.0,
            1.0,
        )

    @staticmethod
    def _average_flow(
        flow_sessions: Sequence[dict],
    ) -> float:
        if not flow_sessions:
            return 0.0

        durations = [
            max(
                0,
                int(session.get("duration_seconds") or 0),
            )
            for session in flow_sessions
        ]

        return sum(durations) / len(durations)

    def _is_focused(self, event: Event) -> bool:
        source = (event.source or "").upper()
        context = (event.context or "").upper()

        return (
            source == self.FOCUSED_CONTEXT
            or context == self.FOCUSED_CONTEXT
        )

    @staticmethod
    def _ratio(
        numerator: float,
        denominator: float,
    ) -> float:
        if denominator <= 0:
            return 0.0

        return FlowScoreCalculator._clamp(
            numerator / denominator,
            0.0,
            1.0,
        )

    @staticmethod
    def _clamp(
        value: float,
        minimum: float,
        maximum: float,
    ) -> float:
        return max(
            minimum,
            min(maximum, value),
        )