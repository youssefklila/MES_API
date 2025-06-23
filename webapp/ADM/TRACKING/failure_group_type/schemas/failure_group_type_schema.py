# schemas/failure_group_type_schema.py

from pydantic import BaseModel
from typing import Optional

class FailureGroupTypeBase(BaseModel):
    failure_group_name: str
    failure_group_desc: Optional[str] = None

class FailureGroupTypeCreate(FailureGroupTypeBase):
    pass

class FailureGroupTypeUpdate(BaseModel):
    failure_group_name: Optional[str] = None
    failure_group_desc: Optional[str] = None

class FailureGroupTypeResponse(FailureGroupTypeBase):
    id: int
    
    class Config:
        from_attributes = True
