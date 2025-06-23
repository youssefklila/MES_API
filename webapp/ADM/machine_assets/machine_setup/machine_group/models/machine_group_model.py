# models/machine_group_model.py

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from webapp.database import Base

class MachineGroup(Base):
    __tablename__ = "machine_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cell_id = Column(Integer, ForeignKey("cells.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    failure = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="machine_groups")
    cells = relationship("Cell", back_populates="machine_groups")
    stations = relationship("Station", back_populates="machine_groups")
    part_masters = relationship("PartMaster", back_populates="machine_groups")

    def __repr__(self):
        return (f"<MachineGroup(id={self.id}, name={self.name}, description={self.description}, "
                f"user_id={self.user_id}, cell_id={self.cell_id}, is_active={self.is_active}, "
                f"failure={self.failure})>")
