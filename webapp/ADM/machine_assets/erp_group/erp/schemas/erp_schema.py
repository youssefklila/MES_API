# schemas/erp_group_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ERPGroupBase(BaseModel):
    state: Optional[int] = None
    erpgroup_no: str
    erp_group_description: Optional[str] = None
    erpsystem: Optional[str] = None
    # station_id: Optional[int] = None
    # station_type: Optional[str] = None
    sequential: Optional[bool] = None
    separate_station: Optional[bool] = None
    fixed_layer: Optional[bool] = None
    modified_by: Optional[int] = None
    user_id: Optional[int] = None
    cst_id: Optional[int] = None
    valid: bool

class ERPGroupCreate(ERPGroupBase):
    pass

class ERPGroupUpdate(ERPGroupBase):
    pass

class ERPGroupResponse(ERPGroupBase):
    id: int
    created_on: datetime
    edited_on: datetime

    class Config:
        orm_mode = True
