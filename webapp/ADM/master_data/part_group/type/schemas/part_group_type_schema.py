# schemas/part_group_type_schema.py

from pydantic import BaseModel
from typing import Optional

class PartGroupTypeBase(BaseModel):
    name: str
    description: Optional[str] = None

class PartGroupTypeCreate(PartGroupTypeBase):
    pass

class PartGroupTypeUpdate(PartGroupTypeBase):
    pass

class PartGroupTypeResponse(PartGroupTypeBase):
    id: int

    class Config:
        orm_mode = True
