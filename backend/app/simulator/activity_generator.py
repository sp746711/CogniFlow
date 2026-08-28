"""Generate realistic simulated developer activities."""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta, time

from app.simulator.config import DEFAULT_CONFIG, SimulatorConfig
from app.simulator.developer_profiles import DeveloperProfile
from app.simulator.team_profiles import TeamProfile


@dataclass(frozen=True)
class Activity:
    """A generated activity before it becomes a database event."""

    timestamp: datetime
    source: str
    event_type: str
    context: str
    title: str
    description: str


class ActivityGenerator:
    """Generate activities based on developer behavior."""

    def __init__(
        self,
        config: SimulatorConfig = DEFAULT_CONFIG,
        random_seed: int | None = None,
    ) -> None:
        self.config = config
        self.random = random.Random(
            config.seed if random_seed is None else random_seed
        )

    def generate_for_developer(
        self,
        work_date: datetime,
        developer_profile: DeveloperProfile,
        team_profile: TeamProfile,
    ) -> list[Activity]:
        """Generate a realistic workday activity sequence."""

        start = datetime.combine(
            work_date.date(),
            self.config.work_start,
        )

        end = datetime.combine(
            work_date.date(),
            self.config.work_end,
        )

        event_count = self.random.randint(
            self.config.minimum_events_per_developer,
            self.config.maximum_events_per_developer,
        )

        activities: list[Activity] = []

        current_time = start

        while len(activities) < event_count and current_time < end:
            activity = self._generate_next_activity(
                current_time=current_time,
                developer_profile=developer_profile,
                team_profile=team_profile,
            )

            activities.append(activity)

            gap_minutes = self.random.randint(5, 35)
            current_time += timedelta(minutes=gap_minutes)

        return activities

    def _generate_next_activity(
        self,
        current_time: datetime,
        developer_profile: DeveloperProfile,
        team_profile: TeamProfile,
    ) -> Activity:
        """Choose the next activity using behavior weights."""

        options = [
            (
                "IDE",
                "coding",
                "IDE",
                "Coding",
                "Developer is working on assigned code.",
                developer_profile.coding_weight
                * team_profile.coding_level,
            ),
            (
                "IDE",
                "testing",
                "IDE",
                "Testing",
                "Developer is testing recent changes.",
                developer_profile.testing_weight
                * team_profile.testing_level,
            ),
            (
                "IDE",
                "debugging",
                "IDE",
                "Debugging",
                "Developer is investigating a development issue.",
                developer_profile.debugging_weight,
                ),
            (
                "Slack",
                "message",
                "SLACK",
                "Team communication",
                "Developer is communicating about current work.",
                developer_profile.communication_weight
                * team_profile.communication_level,
            ),
            (
                "Jira",
                "task_update",
                "JIRA",
                "Jira task update",
                "Developer is updating progress on assigned work.",
                developer_profile.jira_weight
                * team_profile.task_update_level,
            ),
            (
                "GitHub",
                "commit",
                "GITHUB",
                "Git commit",
                "Developer is committing a completed code change.",
                developer_profile.github_weight
                * team_profile.github_level,
            ),
        ]

        sources = [item for item in options]
        weights = [max(item[5], 0.01) for item in sources]

        selected = self.random.choices(
            sources,
            weights=weights,
            k=1,
        )[0]

        return Activity(
            timestamp=current_time,
            source=selected[0],
            event_type=selected[1],
            context=selected[2],
            title=selected[3],
            description=selected[4],
        )