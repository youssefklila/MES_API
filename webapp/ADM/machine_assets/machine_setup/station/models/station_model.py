# models/station_model.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    machine_group_id = Column(Integer, ForeignKey("machine_groups.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    info = Column(String, nullable=True)

    # Relationships
    machine_groups = relationship("MachineGroup", back_populates="stations")
    user = relationship("User", back_populates="stations")
    # erp_groups = relationship("ERPGroup", back_populates="stations")
    assign_stations_to_erpgrp = relationship("AssignStationsToErpGrp", back_populates="station")
    measurement_data = relationship("MeasurementData", back_populates="station")
    condition_data = relationship("MachineConditionData", back_populates="station")
    lines = relationship("Line", secondary="line_station_association", back_populates="stations")
    active_workorders = relationship("ActiveWorkorder", back_populates="station")
    iiot_sensor_data = relationship("IIOTSensorData", back_populates="station")
    maintenance_configurations = relationship("MaintenanceConfiguration", back_populates="station")

    def __repr__(self):
        return f"<Station(id={self.id}, machine_group_id={self.machine_group_id}, name={self.name}, description={self.description}, is_active={self.is_active}, user_id={self.user_id}, info={self.info})>"
