from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base

class BomHeader(Base):
    __tablename__ = "bom_headers"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date, nullable=True)
    last_updated = Column(DateTime, nullable=False)
    part_master_id = Column(Integer, ForeignKey("part_master.id", ondelete="CASCADE", deferrable=True, initially="DEFERRED"), nullable=False)

    # Relationships
    part_master = relationship("PartMaster", back_populates="bom_headers")
    bom_items = relationship("BomItem", back_populates="bom_header", cascade="all, delete-orphan")