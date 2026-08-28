"""Main simulator runner for CogniFlow."""

from __future__ import annotations

from datetime import datetime
from typing import Sequence

from app.models.developer import Developer
from app.models.task import Task

from app.simulator.activity_generator import ActivityGenerator
from app.simulator.communication_generator import (
    CommunicationGenerator,
)
from app.simulator.config import (
    DEFAULT_CONFIG,
    SimulatorConfig,
)
from app.simulator.event_generator import (
    EventGenerator,
    GeneratedEvent,
)
from app.simulator.task_generator import TaskGenerator
from app.simulator.team_profiles import get_team_profile


class SimulationRunner:
    """Run one complete simulated CogniFlow workday.

    The runner coordinates:

    - Developer behavior profiles
    - Team behavior profiles
    - Jira task assignments
    - IDE activity
    - Slack communication
    - GitHub activity
    - Unified event generation

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

        self.communication_generator = CommunicationGenerator(
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
        2. Validate the task population.
        3. Assign Jira tasks/bugs to developers.
        4. Generate developer-specific activity.
        5. Associate activities with assigned tasks.
        6. Generate relationship-aware Slack communication.
        7. Convert all activities into unified events.
        8. Return all events in chronological order.

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

        # ----------------------------------------------------------
        # TASK ASSIGNMENTS
        # ----------------------------------------------------------

        task_assignments = self.task_generator.assign_developers(
            task_list
        )

        tasks_by_developer = self._build_developer_task_map(
            task_assignments
        )

        generated_events: list[GeneratedEvent] = []

        # ----------------------------------------------------------
        # DEVELOPER ACTIVITY
        # ----------------------------------------------------------

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

        # ----------------------------------------------------------
        # SLACK COMMUNICATION
        # ----------------------------------------------------------

        communication_events = self._generate_communication_events(
            work_date=work_date,
            developers=developer_list,
            tasks_by_developer=tasks_by_developer,
        )

        generated_events.extend(communication_events)

        # ----------------------------------------------------------
        # FINAL CHRONOLOGICAL ORDER
        # ----------------------------------------------------------

        generated_events.sort(
            key=self._event_sort_key,
        )

        return generated_events

    # ==============================================================
    # DEVELOPER EVENTS
    # ==============================================================

    def _generate_developer_events(
        self,
        *,
        work_date: datetime,
        developer: Developer,
        developer_tasks: Sequence[Task],
    ) -> list[GeneratedEvent]:
        """Generate the complete activity stream for one developer."""

        team_code = self._get_team_code(
            developer
        )

        team_profile = get_team_profile(
            team_code
        )

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

        for activity_index, activity in enumerate(
            activities
        ):
            task = self._select_task(
                developer=developer,
                developer_tasks=developer_tasks,
                activity_index=activity_index,
            )

            generated_event = (
                self.event_generator.from_activity(
                    developer=developer,
                    activity=activity,
                    task=task,
                )
            )

            events.append(
                generated_event
            )

        return events

    # ==============================================================
    # COMMUNICATION EVENTS
    # ==============================================================

    def _generate_communication_events(
        self,
        *,
        work_date: datetime,
        developers: Sequence[Developer],
        tasks_by_developer: dict[int, list[Task]],
    ) -> list[GeneratedEvent]:
        """Generate Slack communication events."""

        communications = (
            self.communication_generator.generate(
                developers=list(developers),
            )
        )

        if not communications:
            return []

        # Use the configured workday start as the deterministic
        # starting point for communication timestamps.
        communication_time = datetime.combine(
            work_date.date(),
            self.config.work_start,
        )

        events: list[GeneratedEvent] = []

        for index, communication in enumerate(
            communications
        ):
            # Spread communication events through the workday.
            timestamp = self._communication_timestamp(
                communication_time,
                index,
                len(communications),
            )

            sender_id = communication.sender.id

            sender_tasks = tasks_by_developer.get(
                sender_id,
                [],
            )

            task = None

            if sender_tasks:
                task = sender_tasks[
                    index % len(sender_tasks)
                ]

            generated_event = (
                self.event_generator.from_communication(
                    communication=communication,
                    timestamp=timestamp,
                    task=task,
                )
            )

            events.append(
                generated_event
            )

        return events

    def _communication_timestamp(
        self,
        start: datetime,
        index: int,
        total: int,
    ) -> datetime:
        """Return a deterministic timestamp for communication."""

        if total <= 1:
            return start

        work_start = datetime.combine(
            start.date(),
            self.config.work_start,
        )

        work_end = datetime.combine(
            start.date(),
            self.config.work_end,
        )

        total_seconds = int(
            (
                work_end - work_start
            ).total_seconds()
        )

        if total_seconds <= 0:
            raise ValueError(
                "Simulation workday end must be after "
                "workday start."
            )

        # Keep communication events inside the workday.
        usable_seconds = max(
            total_seconds - 60,
            1,
        )

        offset = int(
            usable_seconds
            * index
            / (total - 1)
        )

        return work_start + (
            work_end - work_start
        ) * (
            offset / usable_seconds
        )

    # ==============================================================
    # DEVELOPER → TASK MAP
    # ==============================================================

    def _build_developer_task_map(
        self,
        task_assignments,
    ) -> dict[int, list[Task]]:
        """Build developer -> assigned Jira tasks mapping.

        A task may contain multiple developers. Therefore the same
        task can intentionally appear under several developer IDs.
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

    # ==============================================================
    # TASK SELECTION
    # ==============================================================

    def _select_task(
        self,
        *,
        developer: Developer,
        developer_tasks: Sequence[Task],
        activity_index: int,
    ) -> Task | None:
        """Select a deterministic task for an activity."""

        if not developer_tasks:
            return None

        developer_id = (
            developer.id or 0
        )

        index = (
            developer_id
            + activity_index
        ) % len(developer_tasks)

        return developer_tasks[index]

    # ==============================================================
    # VALIDATION
    # ==============================================================

    def _validate_developers(
        self,
        developers: Sequence[Developer],
    ) -> None:
        """Validate the configured simulated population."""

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

        if len(developer_ids) != len(
            set(developer_ids)
        ):
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

    # ==============================================================
    # PROFILE HELPERS
    # ==============================================================

    @staticmethod
    def _get_team_code(
        developer: Developer,
    ) -> str:
        """Return the developer's stable team code."""

        if developer.team is None:
            raise ValueError(
                f"Developer "
                f"{developer.developer_code} "
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

        return get_developer_profile(
            profile_name
        )

    # ==============================================================
    # EVENT SORTING
    # ==============================================================

    @staticmethod
    def _event_sort_key(
        event: GeneratedEvent,
    ) -> tuple:
        """Provide stable chronological ordering."""

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