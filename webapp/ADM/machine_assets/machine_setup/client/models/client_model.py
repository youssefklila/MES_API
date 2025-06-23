"""Models module."""

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from webapp.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    company_code = Column(String, unique=True)
    name = Column(String, unique=True)
    description = Column(String)
    companies = relationship("CompanyCode", back_populates="client")
    work_plans = relationship("WorkPlan", back_populates="client")

    # Relationship to link Client with User

    def __repr__(self):
        return f"<Client(id={self.id}, user_id={self.user_id}, company_code=\"{self.company_code}\", name=\"{self.name}\", description=\"{self.description}\")>"