# models/failure_type_model.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base

class FailureType(Base):
    __tablename__ = "failure_types"
    __table_args__ = {'extend_existing': True}

    failure_type_id = Column(Integer, primary_key=True, index=True)
    failure_type_code = Column(String(20), nullable=False, unique=True)
    failure_type_desc = Column(String(120), nullable=True)
    site_id = Column(Integer, nullable=True)
    failure_group_id = Column(Integer, ForeignKey("failure_group_types.id"), nullable=True)

    # Relationships
    bookings = relationship("Booking", back_populates="failure_type")
    failure_group = relationship("FailureGroupType", back_populates="failure_types")

    def __repr__(self):
        return f"<FailureType(failure_type_id={self.failure_type_id}, failure_type_code={self.failure_type_code}, failure_type_desc={self.failure_type_desc}, site_id={self.site_id})>"
