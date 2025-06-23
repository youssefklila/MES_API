# schemas/bom_schema.py

from pydantic import BaseModel
from datetime import date
from typing import Optional

class BomBase(BaseModel):
    state: str
    bom_type: str
    bom_version: int
    bom_version_valid_from: date
    bom_version_valid_to: Optional[date] = None
    user_id: int
    part_number: int

class BomCreate(BomBase):
    pass

class BomUpdate(BaseModel):
    state: Optional[str] = None
    bom_type: Optional[str] = None
    bom_version: Optional[int] = None
    bom_version_valid_from: Optional[date] = None
    bom_version_valid_to: Optional[date] = None
    user_id: Optional[int] = None
    part_number: Optional[int] = None

class BomResponse(BomBase):
    id: int

    class Config:
        from_attributes = True 