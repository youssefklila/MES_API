from pydantic import BaseModel, ConfigDict
from typing import Optional

class PartMasterBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    part_number: str
    description: Optional[str]
    part_status: Optional[str]
    parttype_id: int
    partgroup_id: Optional[int]
    case_type: Optional[str]
    product: Optional[bool]
    panel: Optional[bool]
    variant: Optional[bool]
    machine_group_id: Optional[int]
    material_info: Optional[str]
    parts_index: Optional[int]
    edit_order_based_bom: Optional[bool]
    site_id: Optional[int]
    unit_id: Optional[int]
    material_code: Optional[str]
    no_of_panels: Optional[int]
    customer_material_number: Optional[str]
    created_on: Optional[str]
    modified_on: Optional[str]

class PartMasterCreate(PartMasterBase):
    pass

class PartMasterUpdate(PartMasterBase):
    pass

class PartMasterResponse(PartMasterBase):
    id: int
