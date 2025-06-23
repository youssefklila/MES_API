"""Task model module."""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from IIOT.database import Base
from datetime import datetime

class Task(Base):
    """Task model class."""
    __tablename__ = "monitoring_tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationship with User
    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, " \
               f"description=\"{self.description}\", " \
               f"priority=\"{self.priority}\", " \
               f"created_at=\"{self.created_at}\", " \
               f"assigned_to={self.assigned_to})>"
