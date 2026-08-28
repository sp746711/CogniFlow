"""Seed simulated Jira tasks and bugs for CogniFlow."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.developer import Developer
from app.models.task import Task
from app.models.team import Team


TASK_DATA = [
    {
        "task_key": "FEAT-101",
        "title": "Implement user profile API",
        "description": "Create the API required for user profile operations.",
        "issue_type": "Task",
        "status": "In Progress",
        "priority": "High",
        "team_code": "ALPHA",
        "developers": ["DEV001", "DEV003"],
    },
    {
        "task_key": "BUG-102",
        "title": "Fix authentication failure",
        "description": "Investigate and fix an authentication-related failure.",
        "issue_type": "Bug",
        "status": "In Progress",
        "priority": "High",
        "team_code": "ALPHA",
        "developers": ["DEV003", "DEV005"],
    },
    {
        "task_key": "FEAT-103",
        "title": "Improve API response validation",
        "description": "Improve validation for application API responses.",
        "issue_type": "Task",
        "status": "To Do",
        "priority": "Medium",
        "team_code": "ALPHA",
        "developers": ["DEV002"],
    },
    {
        "task_key": "FEAT-201",
        "title": "Build analytics endpoint",
        "description": "Create backend endpoints for analytics information.",
        "issue_type": "Task",
        "status": "In Progress",
        "priority": "High",
        "team_code": "BETA",
        "developers": ["DEV006", "DEV008"],
    },
    {
        "task_key": "BUG-202",
        "title": "Fix database query timeout",
        "description": "Investigate slow database queries and improve performance.",
        "issue_type": "Bug",
        "status": "In Progress",
        "priority": "High",
        "team_code": "BETA",
        "developers": ["DEV007", "DEV009"],
    },
    {
        "task_key": "TASK-203",
        "title": "Add API error handling",
        "description": "Improve error handling across backend endpoints.",
        "issue_type": "Task",
        "status": "To Do",
        "priority": "Medium",
        "team_code": "BETA",
        "developers": ["DEV010"],
    },
    {
        "task_key": "FEAT-301",
        "title": "Create dashboard components",
        "description": "Build the dashboard component structure.",
        "issue_type": "Task",
        "status": "In Progress",
        "priority": "High",
        "team_code": "GAMMA",
        "developers": ["DEV011", "DEV013"],
    },
    {
        "task_key": "BUG-302",
        "title": "Fix dashboard rendering issue",
        "description": "Investigate and fix an intermittent dashboard rendering issue.",
        "issue_type": "Bug",
        "status": "Open",
        "priority": "Medium",
        "team_code": "GAMMA",
        "developers": ["DEV012", "DEV014"],
    },
    {
        "task_key": "TASK-303",
        "title": "Improve dashboard navigation",
        "description": "Improve navigation between dashboard sections.",
        "issue_type": "Task",
        "status": "To Do",
        "priority": "Low",
        "team_code": "GAMMA",
        "developers": ["DEV015"],
    },
    {
        "task_key": "TASK-401",
        "title": "Create automated test coverage",
        "description": "Increase automated testing coverage for application features.",
        "issue_type": "Task",
        "status": "In Progress",
        "priority": "High",
        "team_code": "DELTA",
        "developers": ["DEV016", "DEV018"],
    },
    {
        "task_key": "BUG-402",
        "title": "Fix failing integration test",
        "description": "Investigate and resolve a failing integration test.",
        "issue_type": "Bug",
        "status": "Open",
        "priority": "High",
        "team_code": "DELTA",
        "developers": ["DEV017", "DEV019"],
    },
    {
        "task_key": "TASK-403",
        "title": "Review regression results",
        "description": "Review regression test results and update task status.",
        "issue_type": "Task",
        "status": "To Do",
        "priority": "Medium",
        "team_code": "DELTA",
        "developers": ["DEV020"],
    },
    {
        "task_key": "TASK-501",
        "title": "Improve application deployment",
        "description": "Improve the simulated deployment workflow.",
        "issue_type": "Task",
        "status": "In Progress",
        "priority": "High",
        "team_code": "OMEGA",
        "developers": ["DEV021", "DEV023"],
    },
    {
        "task_key": "BUG-502",
        "title": "Fix service health check",
        "description": "Investigate and fix service health-check failures.",
        "issue_type": "Bug",
        "status": "Open",
        "priority": "High",
        "team_code": "OMEGA",
        "developers": ["DEV022", "DEV024"],
    },
    {
        "task_key": "TASK-503",
        "title": "Improve service monitoring",
        "description": "Improve monitoring-related workflow activity.",
        "issue_type": "Task",
        "status": "To Do",
        "priority": "Medium",
        "team_code": "OMEGA",
        "developers": ["DEV025"],
    },
]


def seed_tasks(db: Session) -> list[Task]:
    """
    Create realistic simulated Jira tasks and bugs.

    Tasks belong to teams and may involve one or multiple developers.
    """

    teams = {
        team.code: team
        for team in db.scalars(select(Team)).all()
    }

    developers = {
        developer.developer_code: developer
        for developer in db.scalars(select(Developer)).all()
    }

    if len(teams) != 5:
        raise ValueError(
            "Exactly 5 teams must exist before seeding tasks."
        )

    if len(developers) != 25:
        raise ValueError(
            "Exactly 25 developers must exist before seeding tasks."
        )

    tasks: list[Task] = []

    for data in TASK_DATA:
        existing_task = db.scalar(
            select(Task).where(
                Task.task_key == data["task_key"]
            )
        )

        if existing_task:
            tasks.append(existing_task)
            continue

        team_code = data["team_code"]

        if team_code not in teams:
            raise ValueError(
                f"Unknown team code: {team_code}"
            )

        team = teams[team_code]

        task = Task(
            task_key=data["task_key"],
            title=data["title"],
            description=data["description"],
            issue_type=data["issue_type"],
            status=data["status"],
            priority=data["priority"],
            team_id=team.id,
        )

        for developer_code in data["developers"]:
            developer = developers.get(developer_code)

            if developer is None:
                raise ValueError(
                    f"Unknown developer code: {developer_code}"
                )

            if developer.team_id != team.id:
                raise ValueError(
                    f"{developer_code} does not belong to "
                    f"team {team_code}."
                )

            task.developers.append(developer)

        db.add(task)
        tasks.append(task)

    db.flush()

    return tasks