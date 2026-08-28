"""Seed simulated Jira tasks and bugs for CogniFlow.

The five CogniFlow teams remain fixed.

Tasks are deterministic seed data used as the starting Jira-style
workload. Dynamic activity such as events, commits, communication,
interruptions, context switches, and metrics is generated separately
by the simulator.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.developer import Developer
from app.models.task import Task
from app.models.team import Team


# ============================================================================
# INITIAL TASK DATA
# ============================================================================
#
# These are only the initial simulated Jira-style tasks.
#
# The teams are fixed:
#   ALPHA
#   BETA
#   GAMMA
#   DELTA
#   OMEGA
#
# The data generated around these tasks later by CogniFlow's simulator
# should be dynamic and relationship-aware.
#
# Each team starts with three tasks:
#   - feature/task
#   - bug
#   - supporting task
#
# Developers are assigned from the same team only.
#

TASK_DATA = [
    # ------------------------------------------------------------------------
    # ALPHA - Product Development
    # ------------------------------------------------------------------------
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
        "task_key": "TASK-103",
        "title": "Improve API response validation",
        "description": "Improve validation for application API responses.",
        "issue_type": "Task",
        "status": "To Do",
        "priority": "Medium",
        "team_code": "ALPHA",
        "developers": ["DEV002"],
    },

    # ------------------------------------------------------------------------
    # BETA - Backend / API
    # ------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------
    # GAMMA - Frontend / UX
    # ------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------
    # DELTA - Quality Engineering
    # ------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------
    # OMEGA - Platform / Infrastructure
    # ------------------------------------------------------------------------
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


# ============================================================================
# VALIDATION
# ============================================================================


def _validate_task_data() -> None:
    """Validate the static seed configuration before inserting data."""

    if len(TASK_DATA) != 15:
        raise ValueError(
            "CogniFlow requires exactly 15 initial tasks "
            "(3 tasks for each of 5 teams)."
        )

    team_codes = {
        data["team_code"]
        for data in TASK_DATA
    }

    expected_team_codes = {
        "ALPHA",
        "BETA",
        "GAMMA",
        "DELTA",
        "OMEGA",
    }

    if team_codes != expected_team_codes:
        raise ValueError(
            "Task data must contain all five CogniFlow team codes."
        )

    task_keys = [
        data["task_key"]
        for data in TASK_DATA
    ]

    if len(task_keys) != len(set(task_keys)):
        raise ValueError(
            "Duplicate task keys found in TASK_DATA."
        )


# ============================================================================
# SEED TASKS
# ============================================================================


def seed_tasks(db: Session) -> list[Task]:
    """
    Create the initial simulated Jira tasks and bugs.

    The five teams and twenty-five developers are fixed seed entities.

    Tasks are also deterministic and idempotent, but the activity generated
    around these tasks is intentionally handled separately by the simulator.

    Running this function multiple times will not create duplicate tasks.
    """

    _validate_task_data()

    # ------------------------------------------------------------------------
    # Load the five fixed teams.
    # ------------------------------------------------------------------------

    teams = {
        team.code: team
        for team in db.scalars(
            select(Team).order_by(Team.id)
        ).all()
    }

    if len(teams) != 5:
        raise ValueError(
            "Exactly 5 teams must exist before seeding tasks."
        )

    expected_team_codes = {
        "ALPHA",
        "BETA",
        "GAMMA",
        "DELTA",
        "OMEGA",
    }

    if set(teams.keys()) != expected_team_codes:
        raise ValueError(
            "The database must contain the five expected CogniFlow teams."
        )

    # ------------------------------------------------------------------------
    # Load the 25 fixed developers.
    # ------------------------------------------------------------------------

    developers = {
        developer.developer_code: developer
        for developer in db.scalars(
            select(Developer).order_by(Developer.id)
        ).all()
    }

    if len(developers) != 25:
        raise ValueError(
            "Exactly 25 developers must exist before seeding tasks."
        )

    tasks: list[Task] = []

    # ------------------------------------------------------------------------
    # Create tasks.
    # ------------------------------------------------------------------------

    for data in TASK_DATA:
        task_key = data["task_key"]

        existing_task = db.scalar(
            select(Task).where(
                Task.task_key == task_key
            )
        )

        # Idempotent behavior:
        # existing task is reused instead of duplicated.
        if existing_task is not None:
            tasks.append(existing_task)
            continue

        team_code = data["team_code"]

        team = teams.get(team_code)

        if team is None:
            raise ValueError(
                f"Unknown team code: {team_code}"
            )

        task = Task(
            task_key=task_key,
            title=data["title"],
            description=data["description"],
            issue_type=data["issue_type"],
            status=data["status"],
            priority=data["priority"],
            team_id=team.id,
        )

        # --------------------------------------------------------------------
        # Attach developers to the task.
        #
        # A developer can only work on a task belonging to their own team.
        # --------------------------------------------------------------------

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

            if developer not in task.developers:
                task.developers.append(developer)

        db.add(task)
        tasks.append(task)

    # Make newly-created tasks available to the caller before commit.
    db.flush()

    return tasks


# ============================================================================
# OPTIONAL COMMAND-LINE ENTRY POINT
# ============================================================================


def main() -> None:
    """Seed tasks from the command line."""

    from app.core.database import SessionLocal

    db = SessionLocal()

    try:
        tasks = seed_tasks(db)
        db.commit()

        print(
            f"Successfully seeded {len(tasks)} tasks."
        )

        for task in tasks:
            print(
                f"- {task.task_key}: "
                f"{task.title} -> Team ID {task.team_id}"
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()