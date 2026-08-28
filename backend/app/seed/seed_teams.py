"""Seed the five simulated CogniFlow teams."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.team import Team


TEAM_DATA = [
    {
        "name": "Alpha",
        "code": "ALPHA",
        "description": "Product development and application features.",
    },
    {
        "name": "Beta",
        "code": "BETA",
        "description": "Backend services and API development.",
    },
    {
        "name": "Gamma",
        "code": "GAMMA",
        "description": "Frontend and user experience development.",
    },
    {
        "name": "Delta",
        "code": "DELTA",
        "description": "Quality engineering and reliability work.",
    },
    {
        "name": "Omega",
        "code": "OMEGA",
        "description": "Platform and infrastructure development.",
    },
]


def seed_teams(db: Session) -> list[Team]:
    """
    Create the five simulated CogniFlow teams.

    The function is idempotent:
    running it again will not create duplicate teams.
    """

    teams: list[Team] = []

    for data in TEAM_DATA:
        existing_team = db.scalar(
            select(Team).where(Team.code == data["code"])
        )

        if existing_team:
            teams.append(existing_team)
            continue

        team = Team(**data)
        db.add(team)
        teams.append(team)

    db.flush()

    return teams