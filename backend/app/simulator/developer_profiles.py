"""Developer behavior profiles for the CogniFlow simulator."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DeveloperProfile:
    """Describes an individual developer's simulated behavior."""

    name: str
    coding_weight: float
    communication_weight: float
    testing_weight: float
    debugging_weight: float
    jira_weight: float
    github_weight: float


DEVELOPER_PROFILES = (
    DeveloperProfile(
        name="Focused",
        coding_weight=0.90,
        communication_weight=0.20,
        testing_weight=0.45,
        debugging_weight=0.45,
        jira_weight=0.35,
        github_weight=0.65,
    ),
    DeveloperProfile(
        name="Collaborative",
        coding_weight=0.70,
        communication_weight=0.80,
        testing_weight=0.40,
        debugging_weight=0.30,
        jira_weight=0.55,
        github_weight=0.55,
    ),
    DeveloperProfile(
        name="Balanced",
        coding_weight=0.70,
        communication_weight=0.50,
        testing_weight=0.55,
        debugging_weight=0.45,
        jira_weight=0.55,
        github_weight=0.60,
    ),
    DeveloperProfile(
        name="Testing Focused",
        coding_weight=0.45,
        communication_weight=0.40,
        testing_weight=0.90,
        debugging_weight=0.75,
        jira_weight=0.65,
        github_weight=0.40,
    ),
    DeveloperProfile(
        name="Task Driven",
        coding_weight=0.60,
        communication_weight=0.30,
        testing_weight=0.50,
        debugging_weight=0.40,
        jira_weight=0.85,
        github_weight=0.60,
    ),
)


def get_developer_profile(
    profile_name: str,
) -> DeveloperProfile:
    """Return a developer behavior profile."""

    normalized_name = profile_name.strip().lower()

    for profile in DEVELOPER_PROFILES:
        if profile.name.lower() == normalized_name:
            return profile

    raise ValueError(
        f"Unknown developer behavior profile: {profile_name}"
    )