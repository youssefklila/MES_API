from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base

class PartGroup(Base):
    __tablename__ = "part_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    part_type = Column(String, nullable=True)
    costs = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    circulating_lot = Column(Integer, nullable=True)
    automatic_emptying = Column(Integer, nullable=True)  # in days
    master_workplan = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    state = Column(Integer, nullable=True)
    material_transfer = Column(Boolean, default=False)
    created_on = Column(String, nullable=True)  # You can change to Date if using DateTime
    edited_on = Column(String, nullable=True)   # You can change to Date if using DateTime
    part_group_type_id = Column(Integer, ForeignKey("part_group_types.id"), nullable=False)

    # Relationships
    part_group_types = relationship("PartGroupType", back_populates="part_groups")
    user = relationship("User", back_populates="part_groups")
    part_masters = relationship("PartMaster", back_populates="part_groups")


    def __repr__(self):
        return f"<PartGroup(id={self.id}, name={self.name}, user_id={self.user_id}, is_active={self.is_active})>"
