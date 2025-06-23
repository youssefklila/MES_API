"""Active Workorder model."""
from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from webapp.database import Base


class ActiveWorkorder(Base):
    """Active Workorder model."""
    
    __tablename__ = "active_workorders"
    
    id = Column(Integer, primary_key=True, index=True)
    workorder_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"), nullable=False)
    station_id = Column(Integer, ForeignKey("stations.id", ondelete="CASCADE"), nullable=False)
    state = Column(Integer, nullable=False)
    
    # Add a check constraint to ensure state is between 0 and 5
    __table_args__ = (
        CheckConstraint('state IN (0, 1, 2, 3, 4, 5)', name='check_state_value'),
    )
    
    # Relationships
    workorder = relationship("WorkOrder", back_populates="active_workorders")
    station = relationship("Station", back_populates="active_workorders")
    
    def __repr__(self):
        return f"<ActiveWorkorder(id={self.id}, workorder_id={self.workorder_id}, station_id={self.station_id}, state={self.state})>"
