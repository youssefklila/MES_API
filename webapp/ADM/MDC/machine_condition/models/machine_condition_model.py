"""Machine Condition model."""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base


class MachineCondition(Base):
    """Machine Condition model."""
    
    __tablename__ = "machine_conditions"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("machine_condition_groups.id"), nullable=False)
    condition_name = Column(String(50), nullable=False, unique=True)
    condition_description = Column(String(200), nullable=True)
    color_rgb = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationship to parent group
    group = relationship("MachineConditionGroup", back_populates="conditions")
    
    # Relationship to condition data
    condition_data = relationship("MachineConditionData", back_populates="condition")
