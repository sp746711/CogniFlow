"""Context-switch analysis for CogniFlow."""

from __future__ import annotations

from typing import Sequence

from app.models.event import Event


class ContextSwitchAnalyzer:
    """Detect transitions between developer activity contexts."""

    VALID_CONTEXTS = {
        "IDE",
        "SLACK",
        "JIRA",
        "GITHUB",
    }

    def analyze(self, events: Sequence[Event]) -> list[dict]:
        """Return chronological context transitions."""

        ordered_events = sorted(
            events,
            key=lambda event: (event.timestamp, event.id or 0),
        )

        switches: list[dict] = []

        previous_event: Event | None = None

        for event in ordered_events:
            if previous_event is None:
                previous_event = event
                continue

            from_context = self.normalize_context(
                previous_event.context,
                previous_event.source,
            )

            to_context = self.normalize_context(
                event.context,
                event.source,
            )

            if from_context == to_context:
                previous_event = event
                continue

            if not from_context or not to_context:
                previous_event = event
                continue

            duration_seconds = int(
                max(
                    0,
                    (
                        event.timestamp
                        - previous_event.timestamp
                    ).total_seconds(),
                )
            )

            switches.append(
                {
                    "from_context": from_context,
                    "to_context": to_context,
                    "timestamp": event.timestamp,
                    "from_event_id": previous_event.id,
                    "to_event_id": event.id,
                    "duration_seconds": duration_seconds,
                }
            )

            previous_event = event

        return switches

    def normalize_context(
        self,
        context: str | None,
        source: str | None = None,
    ) -> str:
        """Normalize event context to one of the four project sources."""

        candidate = (context or "").strip().upper()

        if candidate in self.VALID_CONTEXTS:
            return candidate

        candidate = (source or "").strip().upper()

        if candidate in self.VALID_CONTEXTS:
            return candidate

        return ""

    def count_transitions(
        self,
        events: Sequence[Event],
    ) -> int:
        """Return the number of context changes."""

        return len(self.analyze(events))