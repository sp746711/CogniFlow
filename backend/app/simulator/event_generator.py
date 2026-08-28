"""Convert simulated activities into unified CogniFlow events."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.models.developer import Developer
from app.models.task import Task
from app.simulator.activity_generator import Activity
from app.simulator.communication_generator import Communication


@dataclass(frozen=True)
class GeneratedEvent:
    """Event data ready for database persistence."""

    developer_id: int
    team_id: int
    task_id: int | None
    timestamp: datetime
    source: str
    event_type: str
    context: str
    title: str
    description: str | None
    related_developer_id: int | None
    event_metadata: dict | None


class EventGenerator:
    """Generate unified events from simulator activity."""

    def from_activity(
        self,
        developer: Developer,
        activity: Activity,
        task: Task | None = None,
    ) -> GeneratedEvent:
        """Convert an activity into a unified event."""

        return GeneratedEvent(
            developer_id=developer.id,
            team_id=developer.team_id,
            task_id=task.id if task else None,
            timestamp=activity.timestamp,
            source=activity.source,
            event_type=activity.event_type,
            context=activity.context,
            title=activity.title,
            description=activity.description,
            related_developer_id=None,
            event_metadata={
                "simulated": True,
            },
        )

    def from_communication(
        self,
        communication: Communication,
        timestamp: datetime,
        task: Task | None = None,
    ) -> GeneratedEvent:
        """Convert simulated communication into a unified event."""

        return GeneratedEvent(
            developer_id=communication.sender.id,
            team_id=communication.sender.team_id,
            task_id=task.id if task else None,
            timestamp=timestamp,
            source="Slack",
            event_type="message",
            context="SLACK",
            title="Team communication",
            description=communication.message,
            related_developer_id=communication.receiver.id,
            event_metadata={
                "simulated": True,
                "receiver": communication.receiver.developer_code,
            },
        )