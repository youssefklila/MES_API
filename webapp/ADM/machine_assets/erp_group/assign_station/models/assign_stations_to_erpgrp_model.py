# models/assign_stations_to_erpgrp_model.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base

class AssignStationsToErpGrp(Base):
    __tablename__ = "assign_stations_to_erpgrp"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    erp_group_id = Column(Integer, ForeignKey("erp_groups.id"), nullable=False)
    station_type = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    station = relationship("Station", back_populates="assign_stations_to_erpgrp")
    erp_group = relationship("ERPGroup", back_populates="assign_stations_to_erpgrp")
    user = relationship("User", back_populates="assign_stations_to_erpgrp")

    def __repr__(self):
        return (
            f"<AssignStationsToErpGrp(id={self.id}, station_id={self.station_id}, "
            f"erp_group_id={self.erp_group_id}, station_type={self.station_type}, user_id={self.user_id})>"
        )
