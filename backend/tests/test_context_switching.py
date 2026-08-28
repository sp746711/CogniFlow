"""Tests for CogniFlow context-switch analytics."""

from datetime import datetime

from app.services.context_switch_analyzer import (
    ContextSwitchAnalyzer,
)


def test_context_switch_analyzer_can_be_created():
    """Context-switch analyzer must initialize correctly."""

    analyzer = ContextSwitchAnalyzer()

    assert analyzer is not None


def test_context_switches_are_detected(
    event_factory,
):
    """Changes between IDE, Slack and Jira should be detected."""

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
            source="Jira",
            event_type="task_update",
            context="JIRA",
        ),
        event_factory(
            timestamp=datetime(2026, 8, 28, 10, 30),
            source="Jira",
            event_type="task_update",
            context="JIRA",
        ),
    ]

    analyzer = ContextSwitchAnalyzer()

    switches = analyzer.analyze(events)

    assert len(switches) == 2

    assert switches[0]["from_context"] == "IDE"
    assert switches[0]["to_context"] == "SLACK"

    assert switches[0]["from_event_id"] == events[0].id
    assert switches[0]["to_event_id"] == events[1].id

    assert switches[0]["duration_seconds"] == 600

    assert switches[1]["from_context"] == "SLACK"
    assert switches[1]["to_context"] == "JIRA"

    assert switches[1]["duration_seconds"] == 600


def test_same_context_is_not_a_switch(
    event_factory,
):
    """Repeated activity inside one context is not a switch."""

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
            event_type="testing",
            context="IDE",
        ),
    ]

    analyzer = ContextSwitchAnalyzer()

    switches = analyzer.analyze(events)

    assert switches == []