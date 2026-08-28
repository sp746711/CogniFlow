"""Seed the 25 simulated CogniFlow developers."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.developer import Developer
from app.models.team import Team


# ==============================================================
# DEVELOPER BEHAVIOR PROFILES
# ==============================================================

# Five different simulated developer behavior profiles.
#
# Each team receives one developer of each profile.
#
# 5 teams × 5 developers = 25 developers
#
# These profiles define the developer's baseline behavior.
# The actual activity data will be dynamically simulated later.

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
            "Frequently communicates with teammates while continuing "
            "development."
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
            "Works primarily on assigned tasks with structured "
            "development activity."
        ),
    },
]


# ==============================================================
# SEED DEVELOPERS
# ==============================================================


def seed_developers(db: Session) -> list[Developer]:
    """
    Create five simulated developers for each of the five teams.

    Total:
        5 teams × 5 developers = 25 developers.

    Developer codes are deterministic and unique.

    Existing developers are reused instead of duplicated.
    """

    # ----------------------------------------------------------
    # Load the five fixed CogniFlow teams
    # ----------------------------------------------------------

    teams = db.scalars(
        select(Team).order_by(Team.id)
    ).all()

    if len(teams) != 5:
        raise ValueError(
            "Exactly 5 teams must exist before seeding developers."
        )

    # ----------------------------------------------------------
    # Validate the five behavior profiles
    # ----------------------------------------------------------

    if len(DEVELOPER_PROFILES) != 5:
        raise ValueError(
            "Exactly 5 developer behavior profiles are required."
        )

    developers: list[Developer] = []

    # ----------------------------------------------------------
    # Create five developers inside every team
    # ----------------------------------------------------------

    for team_index, team in enumerate(teams, start=1):

        for developer_index, profile in enumerate(
            DEVELOPER_PROFILES,
            start=1,
        ):
            # Generates:
            #
            # Team 1 → DEV001 ... DEV005
            # Team 2 → DEV006 ... DEV010
            # Team 3 → DEV011 ... DEV015
            # Team 4 → DEV016 ... DEV020
            # Team 5 → DEV021 ... DEV025

            developer_number = (
                (team_index - 1) * 5
            ) + developer_index

            developer_code = f"DEV{developer_number:03d}"

            # --------------------------------------------------
            # Prevent duplicate developers
            # --------------------------------------------------

            existing_developer = db.scalar(
                select(Developer).where(
                    Developer.developer_code == developer_code
                )
            )

            if existing_developer is not None:
                developers.append(existing_developer)
                continue

            # --------------------------------------------------
            # Create developer
            # --------------------------------------------------

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

    # Make newly created developers available immediately.
    db.flush()

    return developers


# ==============================================================
# COMMAND-LINE ENTRY POINT
# ==============================================================


def main() -> None:
    """
    Seed the 25 simulated CogniFlow developers.
    """

    db = SessionLocal()

    try:
        developers = seed_developers(db)

        db.commit()

        print(
            f"Successfully seeded {len(developers)} developers."
        )

        # Show a simple verification list.
        for developer in developers:
            print(
                f"  - {developer.developer_code}: "
                f"{developer.name} "
                f"-> Team ID {developer.team_id}"
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()