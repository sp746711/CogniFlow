"""CogniFlow FastAPI application."""

from fastapi import FastAPI

from app.api.routes.context_switching import router as context_switching_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.developers import router as developers_router
from app.api.routes.events import router as events_router
from app.api.routes.flow import router as flow_router
from app.api.routes.interruptions import router as interruptions_router
from app.api.routes.recovery import router as recovery_router
from app.api.routes.reports import router as reports_router
from app.api.routes.simulation import router as simulation_router
from app.api.routes.tasks import router as tasks_router
from app.api.routes.teams import router as teams_router


app = FastAPI(
    title="CogniFlow API",
    description=(
        "Developer flow-state and workflow analytics platform "
        "using simulated IDE, Slack, Jira and GitHub activity."
    ),
    version="1.0.0",
)


app.include_router(teams_router, prefix="/api")
app.include_router(developers_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(events_router, prefix="/api")
app.include_router(simulation_router, prefix="/api")
app.include_router(flow_router, prefix="/api")
app.include_router(interruptions_router, prefix="/api")
app.include_router(context_switching_router, prefix="/api")
app.include_router(recovery_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(reports_router, prefix="/api")


@app.get("/")
def root() -> dict:
    """Return basic API information."""

    return {
        "name": "CogniFlow API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health_check() -> dict:
    """Return API health status."""

    return {
        "status": "healthy",
    }