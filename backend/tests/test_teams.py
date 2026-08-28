"""Tests for CogniFlow teams."""

from app.models.team import Team


def test_five_teams_exist(db_session):
    """The simulated company must contain exactly five teams."""

    teams = db_session.query(Team).all()

    assert len(teams) == 5


def test_team_codes_are_unique(db_session):
    """Every simulated team must have a unique code."""

    teams = db_session.query(Team).all()

    codes = [team.code for team in teams]

    assert len(codes) == len(set(codes))


def test_expected_team_codes(db_session):
    """Verify the five configured CogniFlow teams."""

    teams = db_session.query(Team).all()

    codes = {team.code for team in teams}

    assert codes == {
        "ALPHA",
        "BETA",
        "GAMMA",
        "DELTA",
        "OMEGA",
    }