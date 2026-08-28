"""
CogniFlow application configuration.

All environment-specific settings are loaded from environment variables.

CogniFlow uses simulated/demo data only. It does not connect to
real Slack, Jira, GitHub, or IDE services.
"""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv


# ==============================================================
# ENVIRONMENT
# ==============================================================

# Load variables from backend/.env when it exists.
load_dotenv()


# ==============================================================
# SETTINGS
# ==============================================================


class Settings:
    """
    Central application configuration for CogniFlow.

    CogniFlow uses:

    - Python
    - FastAPI
    - PostgreSQL
    - SQLAlchemy
    - Alembic
    - Simulated/demo activity data

    The simulation represents:

    - 5 teams
    - 5 developers per team
    - 25 total developers
    - 10:00 AM - 6:00 PM simulated workday

    No real Slack, Jira, GitHub, or IDE credentials are required.
    """

    # ----------------------------------------------------------
    # Application
    # ----------------------------------------------------------

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
    ).lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

    # ----------------------------------------------------------
    # API
    # ----------------------------------------------------------

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

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    # CogniFlow currently uses synchronous SQLAlchemy sessions.
    #
    # The PostgreSQL driver is psycopg, as configured in
    # requirements.txt.
    #
    # Example:
    #
    # postgresql+psycopg://username:password@host:port/database

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/cogniflow",
    )

    # ----------------------------------------------------------
    # CORS
    # ----------------------------------------------------------

    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:5173",
        ).split(",")
        if origin.strip()
    ]

    # ----------------------------------------------------------
    # CogniFlow Simulation
    # ----------------------------------------------------------

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

    # ----------------------------------------------------------
    # Simulated Workday
    # ----------------------------------------------------------

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

    # ----------------------------------------------------------
    # Simulation Timezone
    # ----------------------------------------------------------

    SIMULATION_TIMEZONE: str = os.getenv(
        "SIMULATION_TIMEZONE",
        "Asia/Kolkata",
    )

    # ----------------------------------------------------------
    # Randomization
    # ----------------------------------------------------------

    RANDOM_SEED: int = int(
        os.getenv(
            "RANDOM_SEED",
            "42",
        )
    )

    # ----------------------------------------------------------
    # Computed Properties
    # ----------------------------------------------------------

    @property
    def workday_start_minutes(self) -> int:
        """
        Return simulated workday start as minutes from midnight.

        Example:
            10:00 AM -> 600 minutes
        """

        return self.WORKDAY_START_HOUR * 60

    @property
    def workday_end_minutes(self) -> int:
        """
        Return simulated workday end as minutes from midnight.

        Example:
            6:00 PM -> 1080 minutes
        """

        return self.WORKDAY_END_HOUR * 60

    @property
    def workday_duration_hours(self) -> int:
        """
        Return the configured simulated workday duration.
        """

        return (
            self.WORKDAY_END_HOUR
            - self.WORKDAY_START_HOUR
        )

    @property
    def simulation_enabled(self) -> bool:
        """
        Return whether CogniFlow is configured for simulation.

        CogniFlow is intentionally a simulated/demo system.
        """

        return True

    @property
    def expected_developer_count(self) -> int:
        """
        Return the expected total number of simulated developers.
        """

        return (
            self.TEAM_COUNT
            * self.DEVELOPERS_PER_TEAM
        )

    # ----------------------------------------------------------
    # Validation
    # ----------------------------------------------------------

    def validate(self) -> None:
        """
        Validate application configuration.

        Raises:
            ValueError: when an invalid configuration is detected.
        """

        # ------------------------------------------------------
        # Team configuration
        # ------------------------------------------------------

        if self.TEAM_COUNT <= 0:
            raise ValueError(
                "TEAM_COUNT must be greater than 0."
            )

        if self.DEVELOPERS_PER_TEAM <= 0:
            raise ValueError(
                "DEVELOPERS_PER_TEAM must be greater than 0."
            )

        if self.TOTAL_DEVELOPERS != (
            self.TEAM_COUNT
            * self.DEVELOPERS_PER_TEAM
        ):
            raise ValueError(
                "TOTAL_DEVELOPERS does not match "
                "TEAM_COUNT × DEVELOPERS_PER_TEAM."
            )

        # ------------------------------------------------------
        # Workday configuration
        # ------------------------------------------------------

        if not (
            0 <= self.WORKDAY_START_HOUR <= 23
        ):
            raise ValueError(
                "WORKDAY_START_HOUR must be between 0 and 23."
            )

        if not (
            1 <= self.WORKDAY_END_HOUR <= 24
        ):
            raise ValueError(
                "WORKDAY_END_HOUR must be between 1 and 24."
            )

        if self.WORKDAY_END_HOUR <= (
            self.WORKDAY_START_HOUR
        ):
            raise ValueError(
                "WORKDAY_END_HOUR must be after "
                "WORKDAY_START_HOUR."
            )

        # ------------------------------------------------------
        # API configuration
        # ------------------------------------------------------

        if not (
            1 <= self.API_PORT <= 65535
        ):
            raise ValueError(
                "API_PORT must be between 1 and 65535."
            )

        if not self.API_HOST.strip():
            raise ValueError(
                "API_HOST cannot be empty."
            )

        if not self.API_PREFIX.strip():
            raise ValueError(
                "API_PREFIX cannot be empty."
            )

        # ------------------------------------------------------
        # Database configuration
        # ------------------------------------------------------

        if not self.DATABASE_URL.strip():
            raise ValueError(
                "DATABASE_URL cannot be empty."
            )

        # ------------------------------------------------------
        # Simulation configuration
        # ------------------------------------------------------

        if not self.SIMULATION_TIMEZONE.strip():
            raise ValueError(
                "SIMULATION_TIMEZONE cannot be empty."
            )


# ==============================================================
# SETTINGS FACTORY
# ==============================================================


@lru_cache
def get_settings() -> Settings:
    """
    Return the cached CogniFlow settings instance.

    Configuration is validated once when the settings object
    is first created.
    """

    settings = Settings()

    settings.validate()

    return settings


# ==============================================================
# GLOBAL SETTINGS INSTANCE
# ==============================================================


settings = get_settings()