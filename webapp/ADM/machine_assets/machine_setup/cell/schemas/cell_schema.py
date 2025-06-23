# schemas/cell_schema.py

from pydantic import BaseModel, ConfigDict
from typing import Optional

class CellBase(BaseModel):
    name: str
    description: Optional[str] = None
    info: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class CellCreate(CellBase):
    site_id: int
    user_id: int

class CellUpdate(CellBase):
    site_id: Optional[int] = None
    user_id: Optional[int] = None

class CellResponse(CellBase):
    id: int
    site_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
