"""Task endpoints module."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from dependency_injector.wiring import inject, Provide
from typing import List, Dict, Any, Optional

from IIOT.containers import Container
from IIOT.monitoring.tasks.schemas import TaskCreate, TaskUpdate, TaskResponse
from IIOT.monitoring.tasks.services.task_service import TaskService
from IIOT.monitoring.tasks.repositories.task_repository import TaskNotFoundError
from IIOT.auth.dependencies import get_current_user, permission_required

router = APIRouter(tags=["Tasks"], prefix="/monitoring/tasks")

# Permission constants
TASK_READ_PERM = "task:read"
TASK_CREATE_PERM = "task:create"
TASK_UPDATE_PERM = "task:update"
TASK_DELETE_PERM = "task:delete"

@router.get("/", response_model=List[TaskResponse])
@inject
async def get_all_tasks(
    task_service: TaskService = Depends(Provide[Container.task_service]),
    current_user: Dict[str, Any] = Depends(permission_required(TASK_READ_PERM))
):
    """Get all tasks (requires task:read permission)."""
    try:
        return task_service.get_all_tasks()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{task_id}", response_model=TaskResponse)
@inject
async def get_task_by_id(
    task_id: int,
    task_service: TaskService = Depends(Provide[Container.task_service]),
    current_user: Dict[str, Any] = Depends(permission_required(TASK_READ_PERM))
):
    """Get task by ID (requires task:read permission)."""
    try:
        return task_service.get_task_by_id(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_task(
    task_data: TaskCreate,
    task_service: TaskService = Depends(Provide[Container.task_service]),
    current_user: Dict[str, Any] = Depends(permission_required(TASK_CREATE_PERM))
):
    """Create a new task (requires task:create permission)."""
    try:
        return task_service.create_task(
            description=task_data.description,
            priority=task_data.priority,
            assigned_to=task_data.assigned_to
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{task_id}", response_model=TaskResponse)
@inject
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    task_service: TaskService = Depends(Provide[Container.task_service]),
    current_user: Dict[str, Any] = Depends(permission_required(TASK_UPDATE_PERM))
):
    """Update task (requires task:update permission)."""
    try:
        # Create kwargs for the update method
        update_data = {}
        if task_data.description is not None:
            update_data["description"] = task_data.description
        if task_data.priority is not None:
            update_data["priority"] = task_data.priority
        if task_data.assigned_to is not None:
            update_data["assigned_to"] = task_data.assigned_to

        return task_service.update_task(task_id, **update_data)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(Provide[Container.task_service]),
    current_user: Dict[str, Any] = Depends(permission_required(TASK_DELETE_PERM))
):
    """Delete task (requires task:delete permission)."""
    try:
        task_service.delete_task(task_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
