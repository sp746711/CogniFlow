"""Seed the 25 simulated CogniFlow developers."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.developer import Developer
from app.models.team import Team


DEVELOPER_PROFILES = [
    {
        "role": "Backend Developer",
        "behavior_profile": "Focused",
        "profile_description": (
            "Spends longer periods coding with relatively few interruptions."
        ),
    },
    {
        "role": "Frontend Developer",
        "behavior_profile": "Collaborative",
        "profile_description": (
            "Frequently communicates with teammates while continuing development."
        ),
    },
    {
        "role": "Full Stack Developer",
        "behavior_profile": "Balanced",
        "profile_description": (
            "Balances coding, task updates, communication, and code activity."
        ),
    },
    {
        "role": "QA Developer",
        "behavior_profile": "Testing Focused",
        "profile_description": (
            "Produces more testing, debugging, and issue-related activity."
        ),
    },
    {
        "role": "Platform Developer",
        "behavior_profile": "Task Driven",
        "profile_description": (
            "Works primarily on assigned tasks with structured development activity."
        ),
]


def seed_developers(db: Session) -> list[Developer]:
    """
    Create five simulated developers for each of the five teams.

    Total:
        5 teams × 5 developers = 25 developers.

    Developer codes are deterministic and unique.
    """

    teams = db.scalars(
        select(Team).order_by(Team.id)
    ).all()

    if len(teams) != 5:
        raise ValueError(
            "Exactly 5 teams must exist before seeding developers."
        )

    developers: list[Developer] = []

    for team_index, team in enumerate(teams, start=1):

        for developer_index, profile in enumerate(
            DEVELOPER_PROFILES,
            start=1,
        ):
            developer_number = (
                (team_index - 1) * 5
            ) + developer_index

            developer_code = f"DEV{developer_number:03d}"

            existing_developer = db.scalar(
                select(Developer).where(
                    Developer.developer_code == developer_code
                )
            )

            if existing_developer:
                developers.append(existing_developer)
                continue

            developer = Developer(
                developer_code=developer_code,
                name=f"Developer {developer_number:02d}",
                role=profile["role"],
                behavior_profile=profile["behavior_profile"],
                profile_description=profile["profile_description"],
                team_id=team.id,
            )

            db.add(developer)
            developers.append(developer)

    db.flush()

    return developers