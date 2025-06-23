from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from webapp.database import Base


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(Integer, primary_key=True, index=True)
    
    # Required fields (marked with *)
    workorder_no = Column(String(80), nullable=False, unique=True)
    workorder_type = Column(String(120), nullable=False)
    part_number = Column(String(80), ForeignKey("part_master.part_number"), nullable=False)
    workorder_qty = Column(Numeric(15, 3), nullable=False)
    startdate = Column(DateTime, nullable=False)
    deliverydate = Column(DateTime, nullable=False)
    unit = Column(String(5), nullable=False)
    bom_version = Column(String(30), nullable=False)
    workplan_type = Column(String(3), nullable=False)
    backflush = Column(String(1), nullable=True)
    source = Column(Numeric(1, 0), nullable=True)
    # Optional fields
    workorder_desc = Column(String(80), nullable=True)
    bom_info = Column(String(20), nullable=True)
    workplan_valid_from = Column(DateTime, nullable=True)
    workorder_no_ext = Column(String(40), nullable=True)
    info1 = Column(String(512), nullable=True)
    info2 = Column(String(512), nullable=True)
    info3 = Column(String(512), nullable=True)
    info4 = Column(String(512), nullable=True)
    status = Column(Numeric(3, 0), nullable=True)
    created = Column(DateTime, nullable=True)
    stamp = Column(DateTime, nullable=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    company_id = Column(Integer, ForeignKey("company_codes.id"), nullable=True)
    drawing_no = Column(String(40), nullable=True)
    workorder_state = Column(String(1), nullable=True)
    parent_workorder = Column(String(30), nullable=True)
    controller = Column(String(20), nullable=True)
    info5 = Column(String(512), nullable=True)
    ninfo1 = Column(Numeric(19, 0), nullable=True)
    ninfo2 = Column(Numeric(19, 0), nullable=True)
    bareboard_no = Column(String(80), nullable=True)
    workplan_vers = Column(Integer, ForeignKey("work_plans.id"), nullable=True)
    aps_planning_start_date = Column(DateTime, nullable=True)
    aps_planning_stamp = Column(DateTime, nullable=True)
    aps_planning_end_date = Column(DateTime, nullable=True)
    aps_order_fixation = Column(Numeric(1, 0), nullable=True)
    
    # Relationships
    part_master = relationship("PartMaster", back_populates="work_orders")
    site = relationship("Site", foreign_keys=[site_id], backref="work_orders")
    client = relationship("Client", foreign_keys=[client_id], backref="work_orders")
    company = relationship("CompanyCode", foreign_keys=[company_id], backref="work_orders")
    measurement_data = relationship("MeasurementData", back_populates="workorder")
    active_workorders = relationship("ActiveWorkorder", back_populates="workorder")
    workplan = relationship("WorkPlan", foreign_keys=[workplan_vers], back_populates="work_orders")

    def __repr__(self):
        return f"<WorkOrder(id={self.id}, workorder_no={self.workorder_no}, part_number={self.part_number})>"
