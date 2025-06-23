"""IIOT Sensor Data model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from webapp.database import Base


class IIOTSensorData(Base):
    """IIOT Sensor Data model."""
    
    __tablename__ = "iiot_sensor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=True, index=True)
    date = Column(DateTime, nullable=False, default=func.now())
    value = Column(JSON, nullable=False)  # Now stores a dict (JSON object)
    
    # Relationship
    station = relationship("Station", back_populates="iiot_sensor_data")
    
    def __repr__(self):
        return f"<IIOTSensorData(id={self.id}, station_id={self.station_id}, date={self.date})>"
