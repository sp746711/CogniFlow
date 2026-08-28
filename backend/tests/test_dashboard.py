"""Tests for the CogniFlow dashboard service."""

from app.services.dashboard_service import DashboardService


def test_dashboard_service_can_be_created(db_session):
    """Dashboard service must initialize correctly."""

    service = DashboardService(db_session)

    assert service is not None


def test_dashboard_overview_returns_seeded_company_data(
    db_session,
):
    """Dashboard overview should use the seeded database data."""

    service = DashboardService(db_session)

    result = service.get_overview()

    assert result is not None

    assert result["teams"] == 5
    assert result["developers"] == 25

    # No simulation has been executed in this test yet.
    assert result["events"] == 0
    assert result["flow_sessions"] == 0
    assert result["interruptions"] == 0
    assert result["context_switches"] == 0


def test_developer_summary_returns_real_developer(
    db_session,
):
    """Developer dashboard data should come from the database."""

    service = DashboardService(db_session)

    result = service.get_developer_summary(
        developer_id=1,
    )

    assert result["developer_id"] == 1
    assert result["developer_code"] == "DEV001"

    assert result["events"] == 0
    assert result["flow_sessions"] == 0
    assert result["interruptions"] == 0
    assert result["context_switches"] == 0


def test_developer_rankings_return_seeded_developers(
    db_session,
):
    """Developer rankings should include the simulated workforce."""

    service = DashboardService(db_session)

    rankings = service.get_developer_rankings()

    assert len(rankings) == 25

    codes = {
        item["developer_code"]
        for item in rankings
    }

    assert codes == {
        f"DEV{number:03d}"
        for number in range(1, 26)
    }