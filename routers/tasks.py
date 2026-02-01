"""
Task management endpoints.
In-memory storage with optional query filtering.
"""

from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Query

from schemas.models import Task, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])

# In-memory storage for tasks
tasks_db: list[Task] = []
_task_id_counter = 1


@router.post("", response_model=Task)
def create_task(task: TaskCreate) -> Task:
    """Create a new task."""
    global _task_id_counter
    new_task = Task(id=_task_id_counter, **task.model_dump())
    tasks_db.append(new_task)
    _task_id_counter += 1
    return new_task


@router.get("", response_model=list[Task])
def list_tasks(
    status: Annotated[
        Optional[Literal["todo", "in_progress", "done"]],
        Query(description="Filter by task status"),
    ] = None,
    priority: Annotated[
        Optional[Literal["low", "medium", "high"]],
        Query(description="Filter by task priority"),
    ] = None,
    assigned_to: Annotated[
        Optional[str],
        Query(description="Filter by assigned username"),
    ] = None,
) -> list[Task]:
    """List all tasks with optional filtering."""
    result = tasks_db

    if status is not None:
        result = [t for t in result if t.status == status]
    if priority is not None:
        result = [t for t in result if t.priority == priority]
    if assigned_to is not None:
        result = [t for t in result if t.assigned_to == assigned_to]

    return result
