from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from webapp.database import Base


class WorkStep(Base):
    __tablename__ = "work_steps"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to WorkPlan
    workplan_id = Column(Integer, ForeignKey("work_plans.id"), nullable=False)
    erp_group_id = Column(Integer, ForeignKey("erp_groups.id"), nullable=False)
    
    # Relationships
    erp_group = relationship("ERPGroup")

    # Numeric fields
    step = Column(Numeric(10, 0), nullable=True)
    setup_time = Column(Numeric(10, 3), nullable=True)
    te_person = Column(Numeric(10, 3), nullable=True)
    te_machine = Column(Numeric(10, 3), nullable=True)
    te_time_base = Column(Numeric(10, 3), nullable=True)
    te_qty_base = Column(Numeric(10, 0), nullable=True)
    transport_time = Column(Numeric(10, 3), nullable=True)
    wait_time = Column(Numeric(10, 3), nullable=True)
    status = Column(Numeric(4, 0), nullable=True)
    equ_id = Column(Numeric(19, 0), nullable=True)
    msl_relevant = Column(Numeric(2, 0), nullable=True)
    msl_offset = Column(Numeric(9, 0), nullable=True)
    
    # String fields
    workstep_desc = Column(String(40), nullable=True)
    erp_grp_no = Column(String(20), nullable=True)
    erp_grp_desc = Column(String(40), nullable=True)
    time_unit = Column(String(20), nullable=True)
    setup_flag = Column(String(20), nullable=True)
    workstep_version_erp = Column(String(30), nullable=True)
    info = Column(String(20), nullable=True)
    
    # Char fields
    confirmation = Column(String(20), nullable=True)
    sequentiell = Column(String(20), nullable=True)
    workstep_type = Column(String(20), nullable=True)
    traceflag = Column(String(20), nullable=True)
    
    # Timestamp fields
    stamp = Column(DateTime, nullable=True)
    
    # Relationship
    workplan = relationship("WorkPlan", back_populates="work_steps")

    def __repr__(self):
        return f"<WorkStep(id={self.id}, workplan_id={self.workplan_id}, erp_group_id={self.erp_group_id})>"
