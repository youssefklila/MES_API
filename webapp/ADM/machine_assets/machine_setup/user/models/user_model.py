"""Models module."""

from sqlalchemy import Column, String, Boolean, Integer, JSON
from sqlalchemy.orm import relationship
from webapp.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # 'admin' or 'user'
    permissions = Column(JSON, default=list)  # List of permission strings

    # Your existing relationships...
    clients = relationship("Client", backref="user")
    company_codes = relationship("CompanyCode", back_populates="user")
    cells = relationship("Cell", back_populates="user")
    sites = relationship("Site", back_populates="user")
    machine_groups = relationship("MachineGroup", back_populates="user")
    stations = relationship("Station", back_populates="user")
    assign_stations_to_erpgrp = relationship("AssignStationsToErpGrp", back_populates="user")
    part_types = relationship("PartType", back_populates="user")
    part_groups = relationship("PartGroup", back_populates="user")
    work_plans = relationship("WorkPlan", back_populates="user")
    boms = relationship("Bom", back_populates="user")
    lines = relationship("Line", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, " \
               f"email=\"{self.email}\", " \
               f"hashed_password=\"{self.hashed_password}\", " \
               f"is_active={self.is_active})>"