"""Configuration for the CogniFlow simulator."""

from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True)
class SimulatorConfig:
    """Runtime configuration for simulated developer activity."""

    work_start: time = time(10, 0)
    work_end: time = time(18, 0)

    team_count: int = 5
    developers_per_team: int = 5

    minimum_events_per_developer: int = 8
    maximum_events_per_developer: int = 18

    seed: int = 42

    @property
    def developer_count(self) -> int:
        """Return the expected total developer count."""

        return self.team_count * self.developers_per_team


DEFAULT_CONFIG = SimulatorConfig()