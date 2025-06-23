"""Machine Condition Group model."""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from webapp.database import Base


class MachineConditionGroup(Base):
    """Machine Condition Group model."""
    
    __tablename__ = "machine_condition_groups"

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(50), nullable=False, unique=True)
    group_description = Column(String(200), nullable=True)
    # color_rgb column has been moved to machine_condition table
    is_active = Column(Boolean, default=True)
    
    # Relationship to child conditions
    conditions = relationship("MachineCondition", back_populates="group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MachineConditionGroup(id={self.id}, group_name={self.group_name})>"
