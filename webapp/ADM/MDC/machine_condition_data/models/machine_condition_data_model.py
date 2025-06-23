"""Machine Condition Data model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from webapp.database import Base


class MachineConditionData(Base):
    """Machine Condition Data model."""
    
    __tablename__ = "machine_condition_data"
    
    id = Column(Integer, primary_key=True, index=True)
    date_from = Column(DateTime, nullable=False)
    date_to = Column(DateTime, nullable=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    condition_id = Column(Integer, ForeignKey("machine_conditions.id"), nullable=False)
    level = Column(String(20), nullable=True)
    condition_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    condition_stamp = Column(DateTime, nullable=True)
    condition_type = Column(CHAR(1), nullable=True)
    
    # Relationships
    station = relationship("Station", back_populates="condition_data")
    condition = relationship("MachineCondition", back_populates="condition_data")
