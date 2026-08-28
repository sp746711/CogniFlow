"""Tests for the CogniFlow dashboard service."""

from app.services.dashboard_service import DashboardService


def test_dashboard_service_can_be_created(db_session):
    """Dashboard service must initialize correctly."""

    service = DashboardService(db_session)

    assert service is not None


def test_dashboard_returns_result(db_session):
    """Dashboard service should return dashboard data."""

    service = DashboardService(db_session)

    result = service.get_dashboard()

    assert result is not None