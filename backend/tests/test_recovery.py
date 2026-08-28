"""Tests for CogniFlow recovery analytics."""

from datetime import datetime

from app.services.context_switch_analyzer import (
    ContextSwitchAnalyzer,
)
from app.services.interruption_analyzer import (
    InterruptionAnalyzer,
)
from app.services.recovery_analyzer import RecoveryAnalyzer


def test_recovery_analyzer_can_be_created():
    """Recovery analyzer must initialize correctly."""

    analyzer = RecoveryAnalyzer()

    assert analyzer is not None


def test_recovery_after_slack_interruption(
    event_factory,
):
    """
    Recovery should measure the time from an interruption
    until the next focused IDE event.
    """

    events = [
        event_factory(
            timestamp=datetime(2026, 8, 28, 10, 0),
            source="IDE",
            event_type="coding",
            context="IDE",
        ),
        event_factory(
            timestamp=datetime(2026, 8, 28, 10, 10),
            source="Slack",
            event_type="message",
            context="SLACK",
        ),
        event_factory(
            timestamp=datetime(2026, 8, 28, 10, 20),
            source="IDE",
            event_type="coding",
            context="IDE",
        ),
    ]

    interruption_analyzer = InterruptionAnalyzer()

    interruptions = interruption_analyzer.analyze(events)

    context_analyzer = ContextSwitchAnalyzer()

    context_switches = context_analyzer.analyze(events)

    recovery_analyzer = RecoveryAnalyzer()

    recovery_values = recovery_analyzer.analyze(
        events,
        interruptions,
        context_switches,
    )

    assert recovery_values == [600]

    assert (
        recovery_analyzer.average_recovery_seconds(
            recovery_values
        )
        == 600
    )


def test_no_recovery_without_interruptions_or_switches(
    event_factory,
):
    """A continuous IDE sequence has no recovery event."""

    events = [
        event_factory(
            timestamp=datetime(2026, 8, 28, 10, 0),
            source="IDE",
            event_type="coding",
            context="IDE",
        ),
        event_factory(
            timestamp=datetime(2026, 8, 28, 10, 10),
            source="IDE",
            event_type="coding",
            context="IDE",
        ),
    ]

    interruption_analyzer = InterruptionAnalyzer()
    interruptions = interruption_analyzer.analyze(events)

    context_analyzer = ContextSwitchAnalyzer()
    context_switches = context_analyzer.analyze(events)

    recovery_analyzer = RecoveryAnalyzer()

    recovery_values = recovery_analyzer.analyze(
        events,
        interruptions,
        context_switches,
    )

    assert recovery_values == []