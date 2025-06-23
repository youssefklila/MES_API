from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Optional

class BomHeaderBase(BaseModel):
    description: str
    valid_from: date
    valid_to: Optional[date] = None
    part_master_id: int

class BomHeaderCreate(BomHeaderBase):
    pass

class BomHeaderUpdate(BaseModel):
    description: Optional[str] = None
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    part_master_id: Optional[int] = None

class BomHeaderResponse(BomHeaderBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True