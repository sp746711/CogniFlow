"""
Generate realistic simulated developer activities for CogniFlow.

The activity generator creates simulated activity from:

- IDE
- Slack
- Jira
- GitHub

Activities are generated according to the developer's behavior
profile and the team's activity profile.

This module does not write to the database. Database persistence
is handled by the API/service layer.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta

from app.simulator.config import (
    DEFAULT_CONFIG,
    SimulatorConfig,
)
from app.simulator.developer_profiles import DeveloperProfile
from app.simulator.team_profiles import TeamProfile


# ==============================================================
# ACTIVITY MODEL
# ==============================================================


@dataclass(frozen=True)
class Activity:
    """
    A simulated activity before it becomes a database event.

    EventGenerator later converts this object into a
    GeneratedEvent containing the developer and task relationships.
    """

    timestamp: datetime
    source: str
    event_type: str
    context: str
    title: str
    description: str


# ==============================================================
# ACTIVITY GENERATOR
# ==============================================================


class ActivityGenerator:
    """
    Generate realistic activities for a simulated developer.

    The activity distribution is controlled by:

    - DeveloperProfile
    - TeamProfile
    - SimulatorConfig
    """

    def __init__(
        self,
        config: SimulatorConfig = DEFAULT_CONFIG,
        random_seed: int | None = None,
    ) -> None:
        self.config = config

        self.random = random.Random(
            config.seed
            if random_seed is None
            else random_seed
        )

    # ----------------------------------------------------------
    # PUBLIC GENERATOR
    # ----------------------------------------------------------

    def generate_for_developer(
        self,
        work_date: datetime,
        developer_profile: DeveloperProfile,
        team_profile: TeamProfile,
    ) -> list[Activity]:
        """
        Generate one simulated workday for a developer.

        The number of activities is selected between the configured
        minimum and maximum.

        Every generated activity is kept within the configured
        workday.
        """

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

        # ------------------------------------------------------
        # Generate timestamps across the workday
        # ------------------------------------------------------

        timestamps = self._generate_timestamps(
            start=start,
            end=end,
            count=event_count,
        )

        # ------------------------------------------------------
        # Generate activities using behavior weights
        # ------------------------------------------------------

        for timestamp in timestamps:
            activity = self._generate_next_activity(
                current_time=timestamp,
                developer_profile=developer_profile,
                team_profile=team_profile,
            )

            activities.append(activity)

        return activities

    # ----------------------------------------------------------
    # TIMESTAMP GENERATION
    # ----------------------------------------------------------

    def _generate_timestamps(
        self,
        *,
        start: datetime,
        end: datetime,
        count: int,
    ) -> list[datetime]:
        """
        Generate a deterministic sequence of timestamps.

        The timestamps are spread across the configured workday
        while ensuring that the requested number of activities
        can always be generated.

        A small amount of random variation is used so that events
        do not occur at perfectly fixed intervals.
        """

        if count <= 0:
            return []

        if end <= start:
            raise ValueError(
                "Simulation workday end must be after workday start."
            )

        total_seconds = int(
            (end - start).total_seconds()
        )

        if count == 1:
            return [start]

        # Leave a small boundary so events do not occur exactly
        # at the end of the working day.
        available_seconds = max(
            total_seconds - 60,
            count - 1,
        )

        # Divide the workday into approximately equal sections.
        base_interval = (
            available_seconds // (count - 1)
        )

        timestamps: list[datetime] = []

        for index in range(count):
            if index == 0:
                timestamp = start

            elif index == count - 1:
                timestamp = start + timedelta(
                    seconds=available_seconds
                )

            else:
                base_timestamp = (
                    start
                    + timedelta(
                        seconds=index * base_interval,
                    )
                )

                # Small deterministic variation.
                variation_seconds = self.random.randint(
                    -120,
                    120,
                )

                timestamp = (
                    base_timestamp
                    + timedelta(
                        seconds=variation_seconds,
                    )
                )

            # Ensure the timestamp remains inside the workday.
            if timestamp < start:
                timestamp = start

            latest_timestamp = end - timedelta(
                seconds=60,
            )

            if timestamp > latest_timestamp:
                timestamp = latest_timestamp

            timestamps.append(timestamp)

        # Ensure chronological ordering after random variation.
        timestamps.sort()

        return timestamps

    # ----------------------------------------------------------
    # ACTIVITY SELECTION
    # ----------------------------------------------------------

    def _generate_next_activity(
        self,
        current_time: datetime,
        developer_profile: DeveloperProfile,
        team_profile: TeamProfile,
    ) -> Activity:
        """
        Choose the next activity using developer/team behavior
        weights.
        """

        options = [
            (
                "IDE",
                "coding",
                "IDE",
                "Coding",
                "Developer is working on assigned code.",
                (
                    developer_profile.coding_weight
                    * team_profile.coding_level
                ),
            ),
            (
                "IDE",
                "testing",
                "IDE",
                "Testing",
                "Developer is testing recent changes.",
                (
                    developer_profile.testing_weight
                    * team_profile.testing_level
                ),
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
                (
                    developer_profile.communication_weight
                    * team_profile.communication_level
                ),
            ),
            (
                "Jira",
                "task_update",
                "JIRA",
                "Jira task update",
                "Developer is updating progress on assigned work.",
                (
                    developer_profile.jira_weight
                    * team_profile.task_update_level
                ),
            ),
            (
                "GitHub",
                "commit",
                "GITHUB",
                "Git commit",
                "Developer is committing a completed code change.",
                (
                    developer_profile.github_weight
                    * team_profile.github_level
                ),
            ),
        ]

        weights = [
            max(option[5], 0.01)
            for option in options
        ]

        selected = self.random.choices(
            options,
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