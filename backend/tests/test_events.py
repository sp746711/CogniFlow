"""Tests for unified CogniFlow activity events."""

from datetime import datetime

from app.models.event import Event


VALID_SOURCES = {
    "IDE",
    "Slack",
    "Jira",
    "GitHub",
}


def test_event_source_is_valid(db_session):
    """Events must originate from a simulated source."""

    events = db_session.query(Event).all()

    for event in events:
        assert event.source in VALID_SOURCES


def test_events_have_timestamps(db_session):
    """Every event must have a timestamp."""

    events = db_session.query(Event).all()

    for event in events:
        assert isinstance(event.timestamp, datetime)


def test_events_belong_to_developers(db_session):
    """Events should be associated with simulated developers."""

    events = db_session.query(Event).all()

    for event in events:
        assert event.developer_id is not None