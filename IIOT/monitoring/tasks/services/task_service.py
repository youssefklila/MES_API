"""Task service module."""
from typing import List, Dict, Any, Optional
from IIOT.monitoring.tasks.repositories.task_repository import TaskRepository

class TaskService:
    """Task service class."""

    def __init__(self, task_repository: TaskRepository):
        """Initialize task service."""
        self._repository = task_repository

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks."""
        return self._repository.get_all()

    def get_task_by_id(self, task_id: int) -> Dict[str, Any]:
        """Get task by ID."""
        return self._repository.get_by_id(task_id)

    def create_task(self, description: str, priority: str, assigned_to: Optional[int] = None) -> Dict[str, Any]:
        """Create a new task."""
        return self._repository.add(description, priority, assigned_to)

    def update_task(self, task_id: int, **kwargs) -> Dict[str, Any]:
        """Update task."""
        return self._repository.update(task_id, **kwargs)

    def delete_task(self, task_id: int) -> None:
        """Delete task."""
        self._repository.delete(task_id)
