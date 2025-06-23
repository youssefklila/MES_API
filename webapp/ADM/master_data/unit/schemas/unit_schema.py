# schemas/unit_schema.py

from pydantic import BaseModel
from typing import Optional

class UnitBase(BaseModel):
    unit_name: str
    description: Optional[str] = None

class UnitCreate(UnitBase):
    pass

class UnitUpdate(UnitBase):
    pass

class UnitResponse(UnitBase):
    id: int

    class Config:
        orm_mode = True
