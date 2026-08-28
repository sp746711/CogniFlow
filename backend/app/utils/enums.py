"""Common enums used throughout CogniFlow."""

from enum import Enum


class EventSource(str, Enum):
    """Source system that produced a simulated activity event."""

    IDE = "IDE"
    SLACK = "Slack"
    JIRA = "Jira"
    GITHUB = "GitHub"


class EventType(str, Enum):
    """Types of simulated developer activity."""

    CODING = "coding"
    TESTING = "testing"
    DEBUGGING = "debugging"

    MESSAGE_SENT = "message_sent"
    MESSAGE_RECEIVED = "message_received"

    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_ASSIGNED = "task_assigned"
    BUG_REPORTED = "bug_reported"
    BUG_FIXED = "bug_fixed"

    COMMIT = "commit"
    PULL_REQUEST = "pull_request"
    CODE_REVIEW = "code_review"
    MERGE = "merge"


class IssueType(str, Enum):
    """Simulated Jira issue types."""

    TASK = "Task"
    BUG = "Bug"


class TaskStatus(str, Enum):
    """Simulated Jira task statuses."""

    TO_DO = "To Do"
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class TaskPriority(str, Enum):
    """Simulated Jira task priorities."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class FlowSessionStatus(str, Enum):
    """Status of a developer flow session."""

    ACTIVE = "active"
    COMPLETED = "completed"


class InterruptionType(str, Enum):
    """Types of simulated interruptions."""

    SLACK = "Slack"
    JIRA = "Jira"
    GITHUB = "GitHub"
    IDE = "IDE"


class ContextSwitchType(str, Enum):
    """Common activity-to-activity context switches."""

    IDE_TO_SLACK = "IDE -> Slack"
    SLACK_TO_IDE = "Slack -> IDE"
    IDE_TO_JIRA = "IDE -> Jira"
    JIRA_TO_IDE = "Jira -> IDE"
    IDE_TO_GITHUB = "IDE -> GitHub"
    GITHUB_TO_IDE = "GitHub -> IDE"
    SLACK_TO_JIRA = "Slack -> Jira"
    JIRA_TO_SLACK = "Jira -> Slack"
    SLACK_TO_GITHUB = "Slack -> GitHub"
    GITHUB_TO_SLACK = "GitHub -> Slack"