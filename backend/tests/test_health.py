"""Tests for CogniFlow system health endpoints."""


def test_root_endpoint(client):
    """Root endpoint should return basic API information."""

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "CogniFlow"
    assert data["status"] == "running"


def test_health_endpoint(client):
    """Health endpoint should report API and database status."""

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["database"] == "connected"