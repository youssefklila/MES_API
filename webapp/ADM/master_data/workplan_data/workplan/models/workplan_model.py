from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from webapp.database import Base


class WorkPlan(Base):
    __tablename__ = "work_plans"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    company_id = Column(Integer, ForeignKey("company_codes.id"), nullable=True)
    
    # Numeric fields
    source = Column(Numeric(1, 0), nullable=True)
    status = Column(Numeric(4, 0), nullable=True)
    product_vers_id = Column(Numeric(19, 0), nullable=True)
    
    # String fields
    workplan_status = Column(String(1), nullable=True)
    part_no = Column(String(80), nullable=True)
    part_desc = Column(String(80), nullable=True)
    workplan_desc = Column(String(80), nullable=True)
    workplan_type = Column(String(3), nullable=True)
    workplan_info = Column(String(255), nullable=True)
    workplan_version_erp = Column(String(30), nullable=True)
    aps_info1 = Column(String(4000), nullable=True)
    aps_info2 = Column(String(4000), nullable=True)
    
    # Timestamp fields
    created = Column(DateTime, nullable=True)
    stamp = Column(DateTime, nullable=True)
    workplan_valid_from = Column(DateTime, nullable=True)
    workplan_valid_to = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="work_plans")
    site = relationship("Site", back_populates="work_plans")
    client = relationship("Client", back_populates="work_plans")
    company = relationship("CompanyCode", back_populates="work_plans")
    work_steps = relationship("WorkStep", back_populates="workplan", cascade="all, delete-orphan")
    work_orders = relationship("WorkOrder", back_populates="workplan")

    def __repr__(self):
        return f"<WorkPlan(id={self.id}, part_no={self.part_no}, workplan_desc={self.workplan_desc})>"
