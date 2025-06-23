from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from webapp.database import Base


class PartMaster(Base):
    __tablename__ = "part_master"

    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    part_status = Column(String, nullable=True)
    parttype_id = Column(Integer, ForeignKey("part_types.id"), nullable=False)
    partgroup_id = Column(Integer, ForeignKey("part_groups.id"), nullable=True)
    case_type = Column(String, nullable=True)
    product = Column(Boolean, default=False)
    panel = Column(Boolean, default=False)
    variant = Column(Boolean, default=False)
    machine_group_id = Column(Integer, ForeignKey("machine_groups.id"), nullable=True)
    material_info = Column(String, nullable=True)
    parts_index = Column(Integer, nullable=True)
    edit_order_based_bom = Column(Boolean, default=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=True)
    material_code = Column(String, nullable=True)
    no_of_panels = Column(Integer, nullable=True)
    customer_material_number = Column(String, nullable=True)
    created_on = Column(String, nullable=True)
    modified_on = Column(String, nullable=True)

    part_types = relationship("PartType", back_populates="part_masters")
    part_groups = relationship("PartGroup", back_populates="part_masters")
    machine_groups = relationship("MachineGroup", back_populates="part_masters")
    site = relationship("Site", back_populates="part_masters")
    boms = relationship("Bom", back_populates="part_master")
    bom_headers = relationship("BomHeader", back_populates="part_master")
    bom_items = relationship("BomItem", back_populates="part_master")
    work_orders = relationship("WorkOrder", back_populates="part_master")