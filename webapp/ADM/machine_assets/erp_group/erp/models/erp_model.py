# models/erp_group_model.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from webapp.database import Base

class ERPGroup(Base):
    __tablename__ = "erp_groups"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(Integer, nullable=True)
    erpgroup_no = Column(String, nullable=False)
    erp_group_description = Column(String, nullable=True)
    erpsystem = Column(String, nullable=True)
    # station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    # station_type = Column(String, nullable=True)
    sequential = Column(Boolean, nullable=True)
    separate_station = Column(Boolean, nullable=True)
    fixed_layer = Column(Boolean, nullable=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    edited_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modified_by = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    cst_id = Column(Integer, nullable=True)
    valid = Column(Boolean, nullable=False)

    # Relationships
    # stations = relationship("Station", back_populates="erp_groups")
    assign_stations_to_erpgrp = relationship("AssignStationsToErpGrp", back_populates="erp_group")
