from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base

class Bom(Base):
    __tablename__ = "boms"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, nullable=False)
    bom_type = Column(String, nullable=False)
    bom_version = Column(Integer, nullable=False)
    bom_version_valid_from = Column(Date, nullable=False)
    bom_version_valid_to = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    part_number = Column(Integer, ForeignKey("part_master.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="boms")
    part_master = relationship("PartMaster", back_populates="boms") 