"""Generate relationship-aware simulated Slack communication."""

from __future__ import annotations

import random
from dataclasses import dataclass

from app.models.developer import Developer


@dataclass(frozen=True)
class Communication:
    """A simulated communication event."""

    sender: Developer
    receiver: Developer
    message: str


MESSAGES = (
    "Can you check this issue?",
    "I am investigating the problem now.",
    "The latest change is ready for review.",
    "Can you help test this change?",
    "I found the cause of the issue.",
    "The task has been updated.",
    "Can you review the latest changes?",
)


class CommunicationGenerator:
    """
    Generate realistic developer communication.

    Communication is primarily within the same team. Occasional
    cross-team communication is allowed when useful.
    """

    def __init__(self, seed: int = 42) -> None:
        self.random = random.Random(seed)

    def generate(
        self,
        developers: list[Developer],
        cross_team_probability: float = 0.10,
    ) -> list[Communication]:
        """Generate a limited set of relationship-aware messages."""

        communications: list[Communication] = []

        for sender in developers:
            same_team = [
                developer
                for developer in developers
                if developer.id != sender.id
                and developer.team_id == sender.team_id
            ]

            cross_team = [
                developer
                for developer in developers
                if developer.id != sender.id
                and developer.team_id != sender.team_id
            ]

            if same_team:
                receiver = self.random.choice(same_team)

                communications.append(
                    Communication(
                        sender=sender,
                        receiver=receiver,
                        message=self.random.choice(MESSAGES),
                    )
                )

            if (
                cross_team
                and self.random.random() < cross_team_probability
            ):
                receiver = self.random.choice(cross_team)

                communications.append(
                    Communication(
                        sender=sender,
                        receiver=receiver,
                        message=self.random.choice(MESSAGES),
                    )
                )

        return communications