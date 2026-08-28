"""Tests for unified CogniFlow activity events."""

from datetime import datetime

from app.models.event import Event


VALID_SOURCES = {
    "IDE",
    "Slack",
    "Jira",
    "GitHub",
}

VALID_CONTEXTS = {
    "IDE",
    "SLACK",
    "JIRA",
    "GITHUB",
}


def test_event_model_contains_required_fields(
    db_session,
    event_factory,
):
    """An event should contain all required unified timeline fields."""

    event = event_factory(
        timestamp=datetime(2026, 8, 28, 10, 0),
        source="IDE",
        event_type="coding",
        context="IDE",
        title="Coding activity",
        description="Developer is writing code.",
        event_metadata={
            "simulated": True,
        },
    )

    db_session.commit()

    saved_event = db_session.get(Event, event.id)

    assert saved_event is not None
    assert saved_event.developer_id is not None
    assert saved_event.team_id is not None
    assert saved_event.timestamp == datetime(2026, 8, 28, 10, 0)

    assert saved_event.source == "IDE"
    assert saved_event.event_type == "coding"
    assert saved_event.context == "IDE"
    assert saved_event.title == "Coding activity"


def test_event_source_is_valid(
    db_session,
    event_factory,
):
    """Events must originate from a simulated source."""

    for source in VALID_SOURCES:
        event_factory(
            timestamp=datetime(2026, 8, 28, 10, 0),
            source=source,
            event_type="activity",
            context=source.upper(),
        )

    events = db_session.query(Event).all()

    assert len(events) == 4

    assert all(
        event.source in VALID_SOURCES
        for event in events
    )


def test_event_context_is_valid(
    db_session,
    event_factory,
):
    """Events should use one of the unified activity contexts."""

    event_factory(
        timestamp=datetime(2026, 8, 28, 10, 0),
        source="IDE",
        event_type="coding",
        context="IDE",
    )

    event_factory(
        timestamp=datetime(2026, 8, 28, 10, 10),
        source="Slack",
        event_type="message",
        context="SLACK",
    )

    events = db_session.query(Event).all()

    assert events

    assert all(
        event.context in VALID_CONTEXTS
        for event in events
    )


def test_event_metadata_is_stored(
    db_session,
    event_factory,
):
    """Source-specific simulated metadata should be preserved."""

    metadata = {
        "simulated": True,
        "repository": "project-api",
        "commit_hash": "abc123",
    }

    event = event_factory(
        timestamp=datetime(2026, 8, 28, 10, 0),
        source="GitHub",
        event_type="commit",
        context="GITHUB",
        event_metadata=metadata,
    )

    db_session.commit()

    saved_event = db_session.get(Event, event.id)

    assert saved_event is not None
    assert saved_event.event_metadata == metadata