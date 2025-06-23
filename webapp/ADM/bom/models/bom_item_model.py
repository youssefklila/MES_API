from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base

class BomItem(Base):
    __tablename__ = "bom_items"

    id = Column(Integer, primary_key=True, index=True)
    bom_header_id = Column(Integer, ForeignKey("bom_headers.id", ondelete="CASCADE", deferrable=True, initially="DEFERRED"), nullable=False)
    part_master_id = Column(Integer, ForeignKey("part_master.id", ondelete="CASCADE", deferrable=True, initially="DEFERRED"), nullable=False)
    quantity = Column(Integer, nullable=False)
    is_product = Column(Boolean, nullable=False, default=False)
    component_name = Column(String, nullable=False)

    # Relationships
    bom_header = relationship("BomHeader", back_populates="bom_items")
    part_master = relationship("PartMaster", back_populates="bom_items") 