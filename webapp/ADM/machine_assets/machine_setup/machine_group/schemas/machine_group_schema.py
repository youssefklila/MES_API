# schemas/machine_group_schema.py

from pydantic import BaseModel
from typing import Optional

class MachineGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: int
    cell_id: int
    is_active: bool
    failure: bool

class MachineGroupCreate(MachineGroupBase):
    pass

class MachineGroupUpdate(MachineGroupBase):
    name: Optional[str]
    description: Optional[str]
    is_active: Optional[bool]
    failure: Optional[bool]

class MachineGroup(MachineGroupBase):
    id: int

    class Config:
        orm_mode = True
