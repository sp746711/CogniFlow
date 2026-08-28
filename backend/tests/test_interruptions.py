"""Tests for CogniFlow interruption analytics."""

from datetime import datetime

from app.services.interruption_analyzer import (
    InterruptionAnalyzer,
)


def test_interruption_analyzer_can_be_created():
    """Interruption analyzer must initialize correctly."""

    analyzer = InterruptionAnalyzer()

    assert analyzer is not None


def test_slack_activity_interrupts_ide_work(
    event_factory,
):
    """Slack immediately after IDE activity should be an interruption."""

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

    analyzer = InterruptionAnalyzer()

    interruptions = analyzer.analyze(events)

    assert len(interruptions) == 1

    interruption = interruptions[0]

    assert interruption["interruption_type"] == "slack"
    assert interruption["event_id"] == events[1].id
    assert interruption["timestamp"] == events[1].timestamp
    assert interruption["duration_seconds"] == 600


def test_non_focused_previous_activity_is_not_interruption(
    event_factory,
):
    """Slack after Slack should not count as an IDE interruption."""

    events = [
        event_factory(
            timestamp=datetime(2026, 8, 28, 10, 0),
            source="Slack",
            event_type="message",
            context="SLACK",
        ),
        event_factory(
            timestamp=datetime(2026, 8, 28, 10, 10),
            source="Jira",
            event_type="task_update",
            context="JIRA",
        ),
    ]

    analyzer = InterruptionAnalyzer()

    interruptions = analyzer.analyze(events)

    assert interruptions == []