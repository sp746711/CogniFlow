"""Focus-recovery analysis for CogniFlow."""

from __future__ import annotations

from typing import Sequence

from app.models.event import Event


class RecoveryAnalyzer:
    """Measure return to focused IDE activity after workflow changes."""

    FOCUSED_CONTEXT = "IDE"

    def analyze(
        self,
        events: Sequence[Event],
        interruptions: Sequence[dict],
        context_switches: Sequence[dict],
    ) -> list[int]:
        """Calculate recovery durations in seconds.

        Recovery is measured from a relevant interruption/context change
        until the next focused IDE event.

        Exact recovery rules are not specified by the project PDF, so
        this implementation uses the next IDE event as the return point.
        """

        ordered_events = sorted(
            events,
            key=lambda event: (event.timestamp, event.id or 0),
        )

        recovery_values: list[int] = []

        interruption_event_ids = {
            item.get("event_id")
            for item in interruptions
            if item.get("event_id") is not None
        }

        switch_event_ids = {
            item.get("to_event_id")
            for item in context_switches
            if item.get("to_event_id") is not None
        }

        trigger_ids = interruption_event_ids | switch_event_ids

        if not trigger_ids:
            return recovery_values

        for index, event in enumerate(ordered_events):
            if event.id not in trigger_ids:
                continue

            recovery_event = self._find_next_focused_event(
                ordered_events,
                index + 1,
            )

            if recovery_event is None:
                continue

            seconds = int(
                max(
                    0,
                    (
                        recovery_event.timestamp
                        - event.timestamp
                    ).total_seconds(),
                )
            )

            recovery_values.append(seconds)

        return recovery_values

    def average_recovery_seconds(
        self,
        recovery_values: Sequence[int],
    ) -> float:
        """Return average recovery time."""

        if not recovery_values:
            return 0.0

        return sum(recovery_values) / len(recovery_values)

    def _find_next_focused_event(
        self,
        events: Sequence[Event],
        start_index: int,
    ) -> Event | None:
        for event in events[start_index:]:
            if self._is_focused(event):
                return event

        return None

    def _is_focused(self, event: Event) -> bool:
        source = (event.source or "").upper()
        context = (event.context or "").upper()

        return (
            source == self.FOCUSED_CONTEXT
            or context == self.FOCUSED_CONTEXT
        )