"""
CogniFlow application configuration.

All environment-specific settings are loaded from environment variables.
No real external service credentials are required by CogniFlow because
the project uses simulated/demo data only.
"""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv


# Load variables from backend/.env when it exists.
load_dotenv()


class Settings:
    """
    Central application configuration.

    CogniFlow is a student project using:
    - Python
    - FastAPI
    - PostgreSQL
    - Simulated/demo activity data

    No real Slack, Jira, GitHub, or IDE credentials are required.
    """

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    APP_NAME: str = os.getenv(
        "APP_NAME",
        "CogniFlow",
    )

    APP_VERSION: str = os.getenv(
        "APP_VERSION",
        "1.0.0",
    )

    APP_DESCRIPTION: str = os.getenv(
        "APP_DESCRIPTION",
        "Developer Flow-State and Workflow Analytics Platform",
    )

    ENVIRONMENT: str = os.getenv(
        "ENVIRONMENT",
        "development",
    )

    DEBUG: bool = os.getenv(
        "DEBUG",
        "true",
    ).lower() in {"1", "true", "yes", "on"}

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------

    API_HOST: str = os.getenv(
        "API_HOST",
        "127.0.0.1",
    )

    API_PORT: int = int(
        os.getenv(
            "API_PORT",
            "8000",
        )
    )

    API_PREFIX: str = os.getenv(
        "API_PREFIX",
        "/api",
    )

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/cogniflow",
    )

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------

    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:5173",
        ).split(",")
        if origin.strip()
    ]

    # ------------------------------------------------------------------
    # CogniFlow simulation rules
    # ------------------------------------------------------------------

    TEAM_COUNT: int = int(
        os.getenv(
            "TEAM_COUNT",
            "5",
        )
    )

    DEVELOPERS_PER_TEAM: int = int(
        os.getenv(
            "DEVELOPERS_PER_TEAM",
            "5",
        )
    )

    TOTAL_DEVELOPERS: int = (
        TEAM_COUNT * DEVELOPERS_PER_TEAM
    )

    WORKDAY_START_HOUR: int = int(
        os.getenv(
            "WORKDAY_START_HOUR",
            "10",
        )
    )

    WORKDAY_END_HOUR: int = int(
        os.getenv(
            "WORKDAY_END_HOUR",
            "18",
        )
    )

    # ------------------------------------------------------------------
    # Simulator
    # ------------------------------------------------------------------

    SIMULATION_TIMEZONE: str = os.getenv(
        "SIMULATION_TIMEZONE",
        "Asia/Kolkata",
    )

    RANDOM_SEED: int = int(
        os.getenv(
            "RANDOM_SEED",
            "42",
        )
    )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @property
    def workday_start_minutes(self) -> int:
        """Return the simulated workday start as minutes from midnight."""
        return self.WORKDAY_START_HOUR * 60

    @property
    def workday_end_minutes(self) -> int:
        """Return the simulated workday end as minutes from midnight."""
        return self.WORKDAY_END_HOUR * 60

    @property
    def workday_duration_hours(self) -> int:
        """Return the configured simulated workday duration."""
        return (
            self.WORKDAY_END_HOUR
            - self.WORKDAY_START_HOUR
        )

    @property
    def simulation_enabled(self) -> bool:
        """
        Return whether the application is configured for simulation.

        CogniFlow always uses simulated/demo data. This property exists
        mainly to make that configuration explicit to the rest of the
        application.
        """
        return True

    def validate(self) -> None:
        """
        Validate configuration values before the application starts.
        """

        if self.TEAM_COUNT <= 0:
            raise ValueError(
                "TEAM_COUNT must be greater than 0."
            )

        if self.DEVELOPERS_PER_TEAM <= 0:
            raise ValueError(
                "DEVELOPERS_PER_TEAM must be greater than 0."
            )

        if self.WORKDAY_START_HOUR < 0 or self.WORKDAY_START_HOUR > 23:
            raise ValueError(
                "WORKDAY_START_HOUR must be between 0 and 23."
            )

        if self.WORKDAY_END_HOUR < 1 or self.WORKDAY_END_HOUR > 24:
            raise ValueError(
                "WORKDAY_END_HOUR must be between 1 and 24."
            )

        if self.WORKDAY_END_HOUR <= self.WORKDAY_START_HOUR:
            raise ValueError(
                "WORKDAY_END_HOUR must be after WORKDAY_START_HOUR."
            )

        if self.API_PORT <= 0 or self.API_PORT > 65535:
            raise ValueError(
                "API_PORT must be between 1 and 65535."
            )

        if not self.DATABASE_URL.strip():
            raise ValueError(
                "DATABASE_URL cannot be empty."
            )


@lru_cache
def get_settings() -> Settings:
    """
    Return the cached application settings instance.
    """

    settings = Settings()
    settings.validate()

    return settings


settings = get_settings()