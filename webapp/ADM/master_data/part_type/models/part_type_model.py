# models/part_type_model.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from webapp.database import Base

class PartType(Base):
    __tablename__ = "part_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    date_of_creation = Column(DateTime, default=datetime.utcnow)
    date_of_change = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="part_types")
    part_masters = relationship("PartMaster", back_populates="part_types")

    def __repr__(self):
        return f"<PartType(id={self.id}, name={self.name}, is_active={self.is_active})>"
