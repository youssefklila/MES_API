# models/company_code_model.py

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base

class CompanyCode(Base):
    __tablename__ = "company_codes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="company_codes")
    client = relationship("Client", back_populates="companies")
    sites = relationship("Site", back_populates="company_codes")
    work_plans = relationship("WorkPlan", back_populates="company")

    def __repr__(self):
        return f"<CompanyCode(id={self.id}, user_id={self.user_id}, client_id={self.client_id}, name={self.name}, description={self.description})>"
