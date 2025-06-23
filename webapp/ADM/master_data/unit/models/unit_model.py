# models/unit_model.py

from sqlalchemy import Column, Integer, String
from webapp.database import Base

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    unit_name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"<Unit(id={self.id}, unit_name={self.unit_name}, description={self.description})>"
