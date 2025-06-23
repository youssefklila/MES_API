from pydantic import BaseModel
from typing import Optional

class PartGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: int
    part_type: Optional[str] = None
    costs: Optional[int] = None
    is_active: Optional[bool] = True
    circulating_lot: Optional[int] = None
    automatic_emptying: Optional[int] = None  # in days
    master_workplan: Optional[str] = None
    comment: Optional[str] = None
    state: Optional[int] = None
    material_transfer: Optional[bool] = False
    created_on: Optional[str] = None  # Change to Date if DateTime
    edited_on: Optional[str] = None   # Change to Date if DateTime
    part_group_type_id: int

class PartGroupCreate(PartGroupBase):
    pass

class PartGroupUpdate(PartGroupBase):
    pass

class PartGroupResponse(PartGroupBase):
    id: int

    class Config:
        orm_mode = True
