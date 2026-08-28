"""
CogniFlow FastAPI application.

This is the main entry point for the backend API.

CogniFlow uses simulated/demo developer activity from:

- IDE
- Slack
- Jira
- GitHub

The generated activity is stored in PostgreSQL and processed
for developer flow-state and workflow analytics.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.api.routes.context_switching import (
    router as context_switching_router,
)
from app.api.routes.dashboard import (
    router as dashboard_router,
)
from app.api.routes.developers import (
    router as developers_router,
)
from app.api.routes.events import (
    router as events_router,
)
from app.api.routes.flow import (
    router as flow_router,
)
from app.api.routes.interruptions import (
    router as interruptions_router,
)
from app.api.routes.recovery import (
    router as recovery_router,
)
from app.api.routes.reports import (
    router as reports_router,
)
from app.api.routes.simulation import (
    router as simulation_router,
)
from app.api.routes.tasks import (
    router as tasks_router,
)
from app.api.routes.teams import (
    router as teams_router,
)

from app.core.config import settings
from app.core.database import (
    check_database_connection,
    close_database,
)


# ==============================================================
# APPLICATION LIFESPAN
# ==============================================================


@asynccontextmanager
async def lifespan(
    application: FastAPI,
) -> AsyncIterator[None]:
    """
    Manage CogniFlow application startup and shutdown.

    Startup:
        Validate the application configuration and check the
        PostgreSQL connection.

    Shutdown:
        Dispose the SQLAlchemy database engine.
    """

    settings.validate()

    # The database is required by the backend.
    # Do not automatically create tables here.
    # Database schema management is handled by Alembic.
    if not check_database_connection():
        raise RuntimeError(
            "CogniFlow could not connect to PostgreSQL. "
            "Check DATABASE_URL and make sure PostgreSQL is running."
        )

    yield

    close_database()


# ==============================================================
# FASTAPI APPLICATION
# ==============================================================


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


# ==============================================================
# API ROUTES
# ==============================================================


app.include_router(
    teams_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    developers_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    tasks_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    events_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    simulation_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    flow_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    interruptions_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    context_switching_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    recovery_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    dashboard_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    reports_router,
    prefix=settings.API_PREFIX,
)


# ==============================================================
# ROOT ENDPOINT
# ==============================================================


@app.get(
    "/",
    tags=["System"],
)
def root() -> dict[str, str]:
    """
    Return basic CogniFlow API information.
    """

    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


# ==============================================================
# HEALTH ENDPOINT
# ==============================================================


@app.get(
    "/health",
    tags=["System"],
)
def health_check() -> dict[str, object]:
    """
    Return API and database health status.

    The API is considered healthy only when PostgreSQL is
    reachable.
    """

    database_healthy = check_database_connection()

    return {
        "status": (
            "healthy"
            if database_healthy
            else "unhealthy"
        ),
        "database": (
            "connected"
            if database_healthy
            else "unavailable"
        ),
    }