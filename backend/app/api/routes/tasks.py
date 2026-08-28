"""Jira task and bug API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.dependencies import get_db
from app.models.task import Task
from app.schemas.task import TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
) -> list[Task]:
    """Return all simulated Jira tasks and bugs."""

    statement = (
        select(Task)
        .options(
            selectinload(Task.team),
            selectinload(Task.developers),
        )
        .order_by(Task.id)
    )

    return list(db.scalars(statement).all())


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> Task:
    """Return one Jira task or bug."""

    statement = (
        select(Task)
        .options(
            selectinload(Task.team),
            selectinload(Task.developers),
        )
        .where(Task.id == task_id)
    )

    task = db.scalar(statement)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return task