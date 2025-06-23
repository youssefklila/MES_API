from sqlalchemy import Column, Integer, String, DateTime
from webapp.database import Base
from datetime import datetime

class LocalStorage(Base):
    __tablename__ = "maintenance_local_storage"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=False, unique=True, index=True)
    value = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
