"""Task schema module."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    """Base task schema."""
    description: str
    priority: str
    assigned_to: Optional[int] = None

class TaskCreate(TaskBase):
    """Task create schema."""
    pass

class TaskUpdate(BaseModel):
    """Task update schema."""
    description: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[int] = None

class TaskResponse(TaskBase):
    """Task response schema."""
    id: int
    created_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True
