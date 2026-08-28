"""Team behavior profiles for the CogniFlow simulator."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TeamProfile:
    """Describes the general activity characteristics of a team."""

    code: str
    name: str
    focus: str
    communication_level: float
    coding_level: float
    testing_level: float
    task_update_level: float
    github_level: float


TEAM_PROFILES = (
    TeamProfile(
        code="ALPHA",
        name="Alpha",
        focus="Product development",
        communication_level=0.35,
        coding_level=0.80,
        testing_level=0.45,
        task_update_level=0.55,
        github_level=0.65,
    ),
    TeamProfile(
        code="BETA",
        name="Beta",
        focus="Backend and API development",
        communication_level=0.30,
        coding_level=0.85,
        testing_level=0.55,
        task_update_level=0.50,
        github_level=0.75,
    ),
    TeamProfile(
        code="GAMMA",
        name="Gamma",
        focus="Frontend development",
        communication_level=0.45,
        coding_level=0.75,
        testing_level=0.40,
        task_update_level=0.55,
        github_level=0.60,
    ),
    TeamProfile(
        code="DELTA",
        name="Delta",
        focus="Quality engineering",
        communication_level=0.40,
        coding_level=0.45,
        testing_level=0.85,
        task_update_level=0.65,
        github_level=0.45,
    ),
    TeamProfile(
        code="OMEGA",
        name="Omega",
        focus="Platform and infrastructure",
        communication_level=0.30,
        coding_level=0.70,
        testing_level=0.60,
        task_update_level=0.55,
        github_level=0.80,
    ),
)


def get_team_profile(team_code: str) -> TeamProfile:
    """Return the profile for a team code."""

    normalized_code = team_code.upper()

    for profile in TEAM_PROFILES:
        if profile.code == normalized_code:
            return profile

    raise ValueError(
        f"No simulator profile exists for team '{team_code}'."
    )