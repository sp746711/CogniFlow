"""Tests for the CogniFlow simulation API."""

from datetime import datetime

from app.models.event import Event


VALID_SOURCES = {
    "IDE",
    "Slack",
    "Jira",
    "GitHub",
}


def test_simulation_generates_and_persists_events(
    client,
    db_session,
):
    """Simulation should generate and persist developer events."""

    response = client.post(
        "/api/simulation/run",
        params={
            "work_date": "2026-08-28T00:00:00",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Simulation completed."
    assert data["developers"] == 25
    assert data["tasks"] == 15

    assert data["events_generated"] > 0
    assert data["events_persisted"] == data["events_generated"]

    events = (
        db_session.query(Event)
        .order_by(Event.timestamp, Event.id)
        .all()
    )

    assert len(events) == data["events_persisted"]


def test_simulation_events_have_required_fields(
    client,
    db_session,
):
    """Every generated event should contain required unified fields."""

    response = client.post(
        "/api/simulation/run",
        params={
            "work_date": "2026-08-28T00:00:00",
        },
    )

    assert response.status_code == 200

    events = db_session.query(Event).all()

    assert events

    for event in events:
        assert event.id is not None
        assert event.developer_id is not None
        assert event.team_id is not None
        assert isinstance(event.timestamp, datetime)

        assert event.source in VALID_SOURCES

        assert event.event_type
        assert event.context
        assert event.title


def test_simulation_events_are_linked_to_valid_developers(
    client,
    db_session,
):
    """Generated events must reference existing developers."""

    response = client.post(
        "/api/simulation/run",
        params={
            "work_date": "2026-08-28T00:00:00",
        },
    )

    assert response.status_code == 200

    events = db_session.query(Event).all()

    assert events

    developer_ids = {
        developer.id
        for developer in db_session.query(
            __import__(
                "app.models.developer",
                fromlist=["Developer"],
            ).Developer
        ).all()
    }

    assert all(
        event.developer_id in developer_ids
        for event in events
    )