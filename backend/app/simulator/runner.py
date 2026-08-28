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
    """Run one complete simulated CogniFlow workday.

    The runner coordinates the simulator components and produces a
    chronological stream of simulated developer activity.

    No real Slack, Jira, GitHub, or IDE connection is used.
    """

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
        """Generate one complete simulated workday.

        Workflow:

        1. Validate the configured developer population.
        2. Assign Jira tasks/bugs to developers.
        3. Generate developer-specific activity based on behavior.
        4. Associate activities with the developer's assigned tasks.
        5. Convert activities into unified CogniFlow events.
        6. Return all events in chronological order.

        Database persistence is intentionally handled outside the
        simulator.
        """

        self._validate_developers(developers)

        if not tasks:
            raise ValueError(
                "At least one task is required to run the simulation."
            )

        developer_list = list(developers)
        task_list = list(tasks)

        task_assignments = self.task_generator.assign_developers(
            task_list
        )

        tasks_by_developer = self._build_developer_task_map(
            task_assignments
        )

        generated_events: list[GeneratedEvent] = []

        for developer in developer_list:
            developer_tasks = tasks_by_developer.get(
                developer.id,
                [],
            )

            developer_events = self._generate_developer_events(
                work_date=work_date,
                developer=developer,
                developer_tasks=developer_tasks,
            )

            generated_events.extend(developer_events)

        generated_events.sort(
            key=self._event_sort_key,
        )

        return generated_events

    def _generate_developer_events(
        self,
        *,
        work_date: datetime,
        developer: Developer,
        developer_tasks: Sequence[Task],
    ) -> list[GeneratedEvent]:
        """Generate the complete activity stream for one developer."""

        team_code = self._get_team_code(developer)

        team_profile = get_team_profile(team_code)

        developer_profile = self._get_developer_profile(
            developer.behavior_profile
        )

        activities = (
            self.activity_generator.generate_for_developer(
                work_date=work_date,
                developer_profile=developer_profile,
                team_profile=team_profile,
            )
        )

        events: list[GeneratedEvent] = []

        for activity_index, activity in enumerate(activities):
            task = self._select_task(
                developer=developer,
                developer_tasks=developer_tasks,
                activity_index=activity_index,
            )

            generated_event = self.event_generator.from_activity(
                developer=developer,
                activity=activity,
                task=task,
            )

            events.append(generated_event)

        return events

    def _build_developer_task_map(
        self,
        task_assignments,
    ) -> dict[int, list[Task]]:
        """Build developer -> assigned Jira tasks mapping.

        A task may contain multiple developers. Therefore the same task
        can intentionally appear under several developer IDs.

        Example:

            BUG-102
              ├── DEV003
              └── DEV005
        """

        tasks_by_developer: dict[int, list[Task]] = {}

        for assignment in task_assignments:
            task = assignment.task

            for developer in assignment.developers:
                if developer.id is None:
                    continue

                tasks_by_developer.setdefault(
                    developer.id,
                    [],
                ).append(task)

        return tasks_by_developer

    def _select_task(
        self,
        *,
        developer: Developer,
        developer_tasks: Sequence[Task],
        activity_index: int,
    ) -> Task | None:
        """Select a deterministic task for an activity.

        Task selection is deterministic so repeated simulations with
        the same seed/configuration remain reproducible.

        Activities are still generated according to the developer's
        behavior profile.
        """

        if not developer_tasks:
            return None

        developer_id = developer.id or 0

        index = (
            developer_id
            + activity_index
        ) % len(developer_tasks)

        return developer_tasks[index]

    def _validate_developers(
        self,
        developers: Sequence[Developer],
    ) -> None:
        """Validate the configured simulated company population."""

        expected = self.config.developer_count
        received = len(developers)

        if received != expected:
            raise ValueError(
                f"Expected {expected} developers, "
                f"received {received}."
            )

        developer_ids = [
            developer.id
            for developer in developers
            if developer.id is not None
        ]

        if len(developer_ids) != len(set(developer_ids)):
            raise ValueError(
                "Developer IDs must be unique."
            )

        for developer in developers:
            if developer.team is None:
                raise ValueError(
                    f"Developer "
                    f"{developer.developer_code} "
                    "does not have a team."
                )

            if not developer.behavior_profile:
                raise ValueError(
                    f"Developer "
                    f"{developer.developer_code} "
                    "does not have a behavior profile."
                )

    @staticmethod
    def _get_team_code(
        developer: Developer,
    ) -> str:
        """Return the developer's stable team code."""

        if developer.team is None:
            raise ValueError(
                f"Developer {developer.developer_code} "
                "does not have a team."
            )

        if not developer.team.code:
            raise ValueError(
                f"Team for developer "
                f"{developer.developer_code} "
                "does not have a code."
            )

        return developer.team.code

    @staticmethod
    def _get_developer_profile(
        profile_name: str,
    ):
        """Resolve a configured developer behavior profile."""

        from app.simulator.developer_profiles import (
            get_developer_profile,
        )

        return get_developer_profile(profile_name)

    @staticmethod
    def _event_sort_key(
        event: GeneratedEvent,
    ) -> tuple:
        """Provide stable chronological ordering for generated events."""

        timestamp = getattr(
            event,
            "timestamp",
            None,
        )

        developer_id = getattr(
            event,
            "developer_id",
            None,
        )

        event_type = getattr(
            event,
            "event_type",
            "",
        )

        return (
            timestamp or datetime.min,
            developer_id or 0,
            event_type or "",
        )