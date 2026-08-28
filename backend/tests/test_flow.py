"""Tests for CogniFlow flow analytics."""

from datetime import datetime

from app.services.flow_analyzer import FlowAnalyzer


def test_flow_analyzer_can_be_created():
    """Flow analyzer must initialize correctly."""

    analyzer = FlowAnalyzer()

    assert analyzer is not None


def test_flow_analysis_detects_sustained_ide_activity(
    event_factory,
):
    """Continuous IDE activity should become one flow session."""

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
        event_factory(
            timestamp=datetime(2026, 8, 28, 10, 20),
            source="IDE",
            event_type="testing",
            context="IDE",
        ),
    ]

    analyzer = FlowAnalyzer()

    sessions = analyzer.analyze(events)

    assert len(sessions) == 1

    session = sessions[0]

    assert session["focused_event_count"] == 3
    assert session["start_time"] == datetime(
        2026,
        8,
        28,
        10,
        0,
    )
    assert session["end_time"] == datetime(
        2026,
        8,
        28,
        10,
        20,
    )

    assert session["duration_seconds"] == 1200


def test_non_ide_activity_closes_flow_session(
    event_factory,
):
    """A non-IDE activity should separate flow sessions."""

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
        event_factory(
            timestamp=datetime(2026, 8, 28, 10, 20),
            source="Slack",
            event_type="message",
            context="SLACK",
        ),
        event_factory(
            timestamp=datetime(2026, 8, 28, 10, 30),
            source="IDE",
            event_type="coding",
            context="IDE",
        ),
    ]

    analyzer = FlowAnalyzer()

    sessions = analyzer.analyze(events)

    assert len(sessions) == 2

    assert sessions[0]["focused_event_count"] == 2
    assert sessions[1]["focused_event_count"] == 1