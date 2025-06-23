# schemas/failure_type_schema.py

from pydantic import BaseModel
from typing import Optional

class FailureTypeBase(BaseModel):
    failure_type_code: str
    failure_type_desc: Optional[str] = None
    site_id: Optional[int] = None
    failure_group_id: Optional[int] = None

class FailureTypeCreate(FailureTypeBase):
    pass

class FailureTypeUpdate(BaseModel):
    failure_type_code: Optional[str] = None
    failure_type_desc: Optional[str] = None
    site_id: Optional[int] = None
    failure_group_id: Optional[int] = None

class FailureTypeResponse(FailureTypeBase):
    failure_type_id: int
    
    class Config:
        from_attributes = True
