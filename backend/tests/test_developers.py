"""Tests for CogniFlow developers."""

from app.models.developer import Developer


def test_twenty_five_developers_exist(db_session):
    """The simulated company must contain 25 developers."""

    developers = db_session.query(Developer).all()

    assert len(developers) == 25


def test_developer_codes_are_unique(db_session):
    """Developer codes must be unique."""

    developers = db_session.query(Developer).all()

    codes = [
        developer.developer_code
        for developer in developers
    ]

    assert len(codes) == len(set(codes))


def test_developer_codes_cover_dev001_to_dev025(db_session):
    """Verify the deterministic developer code range."""

    developers = db_session.query(Developer).all()

    codes = {
        developer.developer_code
        for developer in developers
    }

    expected = {
        f"DEV{number:03d}"
        for number in range(1, 26)
    }

    assert codes == expected


def test_each_team_has_five_developers(db_session):
    """Every simulated team must contain five developers."""

    developers = db_session.query(Developer).all()

    counts = {}

    for developer in developers:
        counts[developer.team_id] = (
            counts.get(developer.team_id, 0) + 1
        )

    assert len(counts) == 5
    assert all(count == 5 for count in counts.values())


def test_developer_profiles_are_present(db_session):
    """Every developer must have a behavior profile."""

    developers = db_session.query(Developer).all()

    assert all(
        developer.behavior_profile
        for developer in developers
    )