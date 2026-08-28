"""Main simulator runner for CogniFlow."""

from __future__ import annotations

from datetime import datetime
from typing import Sequence

from app.models.developer import Developer
from app.models.task import Task
from app.simulator.activity_generator import ActivityGenerator
from app.simulator.config import DEFAULT_CONFIG, SimulatorConfig
from app.simulator.event_generator import EventGenerator, GeneratedEvent
from app.simulator.task_generator import TaskGenerator
from app.simulator.team_profiles import get_team_profile


class SimulationRunner:
    """Run one simulated CogniFlow workday."""

    def __init__(
        self,
        config: SimulatorConfig = DEFAULT_CONFIG,
    ) -> None:
        self.config = config

        self.activity_generator = ActivityGenerator(
            config=config,
        )

        self.task_generator = TaskGenerator(
            seed=config.seed,
        )

        self.event_generator = EventGenerator()

    def run(
        self,
        work_date: datetime,
        developers: Sequence[Developer],
        tasks: Sequence[Task],
    ) -> list[GeneratedEvent]:
        """
        Generate a complete simulated workday.

        The runner only generates data. Database persistence is handled
        by the application/service layer.
        """

        if len(developers) != self.config.developer_count:
            raise ValueError(
                f"Expected {self.config.developer_count} developers, "
                f"received {len(developers)}."
            )

        generated_events: list[GeneratedEvent] = []

        task_assignments = self.task_generator.assign_developers(
            list(tasks)
        )

        tasks_by_developer: dict[int, list[Task]] = {}

        for assignment in task_assignments:
            for developer in assignment.developers:
                tasks_by_developer.setdefault(
                    developer.id,
                    [],
                ).append(assignment.task)

        for developer in developers:
            team_code = self._get_team_code(developer)

            team_profile = get_team_profile(team_code)

            developer_profile = (
                self._get_developer_profile(
                    developer.behavior_profile
                )
            )

            activities = (
                self.activity_generator.generate_for_developer(
                    work_date=work_date,
                    developer_profile=developer_profile,
                    team_profile=team_profile,
                )
            )

            developer_tasks = tasks_by_developer.get(
                developer.id,
                [],
            )

            for activity in activities:
                task = None

                if developer_tasks:
                    task = self.task_generator.choose_developer_for_task(
                        developer_tasks[
                            self._safe_task_index(
                                developer.id,
                                len(developer_tasks),
                            )
                        ]
                    )

                generated_event = (
                    self.event_generator.from_activity(
                        developer=developer,
                        activity=activity,
                        task=task,
                    )
                )

                generated_events.append(generated_event)

        generated_events.sort(
            key=lambda event: event.timestamp
        )

        return generated_events

    @staticmethod
    def _get_team_code(
        developer: Developer,
    ) -> str:
        """Get a stable team code from the team's database relationship."""

        if developer.team is None:
            raise ValueError(
                f"Developer {developer.developer_code} "
                "does not have a team."
            )

        return developer.team.code

    @staticmethod
    def _get_developer_profile(
        profile_name: str,
    ):
        """Import and resolve the developer behavior profile."""

        from app.simulator.developer_profiles import (
            get_developer_profile,
        )

        return get_developer_profile(profile_name)

    @staticmethod
    def _safe_task_index(
        developer_id: int,
        task_count: int,
    ) -> int:
        """Return a deterministic task index."""

        if task_count <= 0:
            return 0

        return developer_id % task_count