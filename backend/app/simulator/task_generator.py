"""Generate relationships between simulated Jira work and developers."""

from __future__ import annotations

import random
from dataclasses import dataclass

from app.models.developer import Developer
from app.models.task import Task


@dataclass(frozen=True)
class TaskAssignment:
    """A simulated developer assignment for a task."""

    task: Task
    developers: list[Developer]


class TaskGenerator:
    """Generate realistic task participation."""

    def __init__(self, seed: int = 42) -> None:
        self.random = random.Random(seed)

    def assign_developers(
        self,
        tasks: list[Task],
    ) -> list[TaskAssignment]:
        """
        Build task/developer relationships.

        Existing seeded task relationships are preserved.
        """

        assignments: list[TaskAssignment] = []

        for task in tasks:
            developers = list(task.developers)

            if not developers:
                continue

            assignments.append(
                TaskAssignment(
                    task=task,
                    developers=developers,
                )
            )

        return assignments

    def choose_developer_for_task(
        self,
        task: Task,
    ) -> Developer | None:
        """Choose one participating developer for an event."""

        developers = list(task.developers)

        if not developers:
            return None

        return self.random.choice(developers)