from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from webapp.database import Base
from datetime import datetime
import enum
from sqlalchemy.dialects.postgresql import UUID

class ConfigurationState(str, enum.Enum):
    ACTIVE = "ACTIVE"
    NOT_ACTIVE = "NOT_ACTIVE"

class MaintenanceConfiguration(Base):
    __tablename__ = "maintenance_configurations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    url = Column(String, nullable=False)
    port = Column(String, nullable=True)  # New port attribute
    refresh_time = Column(Integer, nullable=False)  # Time in seconds
    state = Column(Enum(ConfigurationState), nullable=False, default=ConfigurationState.ACTIVE)
    action_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to Station
    station_id = Column(Integer, ForeignKey('stations.id'), nullable=True)
    station = relationship('Station', back_populates='maintenance_configurations')
