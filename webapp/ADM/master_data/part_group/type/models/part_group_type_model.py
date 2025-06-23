# models/part_group_type_model.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from webapp.database import Base

class PartGroupType(Base):
    __tablename__ = "part_group_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    # Relationships
    part_groups = relationship("PartGroup", back_populates="part_group_types")


    def __repr__(self):
        return f"<PartGroupType(id={self.id}, name={self.name})>"
