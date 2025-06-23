# models/site_model.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_code_id = Column(Integer, ForeignKey("company_codes.id"), nullable=True)
    site_number = Column(String, nullable=False, unique=True)
    site_external_number = Column(String, nullable=True)
    deletion_priority = Column(Integer, nullable=True)
    geo_coordinates = Column(String, nullable=True)
    description = Column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="sites")
    company_codes = relationship("CompanyCode", back_populates="sites")
    cells = relationship("Cell", back_populates="site")
    part_masters = relationship("PartMaster", back_populates="site")
    work_plans = relationship("WorkPlan", back_populates="site")

    def __repr__(self):
        return (f"<Site(id={self.id}, user_id={self.user_id}, company_code_id={self.company_code_id}, "
                f"site_number={self.site_number}, site_external_number={self.site_external_number}, "
                f"deletion_priority={self.deletion_priority}, geo_coordinates={self.geo_coordinates}, "
                f"description={self.description})>")
