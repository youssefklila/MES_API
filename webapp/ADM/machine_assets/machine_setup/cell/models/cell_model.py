# models/cell_model.py

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from webapp.database import Base

class Cell(Base):
    __tablename__ = "cells"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    info = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationship to link Cell with CompanyCode and User
    site = relationship("Site", back_populates="cells")
    user = relationship("User", back_populates="cells")
    machine_groups = relationship("MachineGroup", back_populates="cells")
    def __repr__(self):
        return f"<Cell(id={self.id}, name={self.name}, description={self.description}, site_id={self.site_id}, user_id={self.user_id}, info={self.info}, is_active={self.is_active})>"
