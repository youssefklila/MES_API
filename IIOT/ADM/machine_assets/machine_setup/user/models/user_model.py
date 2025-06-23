"""Models module."""

from sqlalchemy import Column, String, Boolean, Integer, JSON
from sqlalchemy.orm import relationship
from IIOT.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # 'admin' or 'user'
    permissions = Column(JSON, default=list)  # List of permission strings
    
    # Relationship with Task
    tasks = relationship("Task", back_populates="user")


    def __repr__(self):
        return f"<User(id={self.id}, " \
               f"email=\"{self.email}\", " \
               f"hashed_password=\"{self.hashed_password}\", " \
               f"is_active={self.is_active})>"