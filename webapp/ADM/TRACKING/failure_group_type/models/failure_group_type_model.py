# models/failure_group_type_model.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from webapp.database import Base

class FailureGroupType(Base):
    __tablename__ = "failure_group_types"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    failure_group_name = Column(String(20), nullable=False, unique=True)
    failure_group_desc = Column(String(20), nullable=True)
    
    # Relationships
    failure_types = relationship("FailureType", back_populates="failure_group")

    def __repr__(self):
        return f"<FailureGroupType(id={self.id}, failure_group_name={self.failure_group_name}, failure_group_desc={self.failure_group_desc})>"
