"""Task repository module."""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from IIOT.monitoring.tasks.models.task_model import Task

class TaskNotFoundError(Exception):
    """Task not found error."""
    pass

class TaskRepository:
    """Task repository class."""

    def __init__(self, session_factory):
        """Initialize task repository."""
        self._session_factory = session_factory

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all tasks as dictionaries."""
        with self._session_factory() as session:
            tasks = session.query(Task).all()
            return [
                {
                    "id": task.id,
                    "description": task.description,
                    "priority": task.priority,
                    "created_at": task.created_at,
                    "assigned_to": task.assigned_to
                }
                for task in tasks
            ]

    def get_by_id(self, task_id: int) -> Dict[str, Any]:
        """Get task by ID as dictionary."""
        with self._session_factory() as session:
            task = session.query(Task).get(task_id)
            if task is None:
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            return {
                "id": task.id,
                "description": task.description,
                "priority": task.priority,
                "created_at": task.created_at,
                "assigned_to": task.assigned_to
            }

    def add(self, description: str, priority: str, assigned_to: Optional[int] = None) -> Dict[str, Any]:
        """Add a new task and return as dictionary."""
        with self._session_factory() as session:
            # Convert 0 to None for assigned_to to avoid foreign key violation
            assigned_to = None if assigned_to == 0 else assigned_to
            
            task = Task(
                description=description,
                priority=priority,
                assigned_to=assigned_to
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return {
                "id": task.id,
                "description": task.description,
                "priority": task.priority,
                "created_at": task.created_at,
                "assigned_to": task.assigned_to
            }

    def update(self, task_id: int, **kwargs) -> Dict[str, Any]:
        """Update task and return as dictionary."""
        with self._session_factory() as session:
            task = session.query(Task).get(task_id)
            if task is None:
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            
            for key, value in kwargs.items():
                setattr(task, key, value)
            
            session.commit()
            session.refresh(task)
            return {
                "id": task.id,
                "description": task.description,
                "priority": task.priority,
                "created_at": task.created_at,
                "assigned_to": task.assigned_to
            }

    def delete(self, task_id: int) -> None:
        """Delete task by ID."""
        with self._session_factory() as session:
            task = session.query(Task).get(task_id)
            if task is None:
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            session.delete(task)
            session.commit()
