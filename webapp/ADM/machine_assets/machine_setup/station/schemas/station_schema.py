# schemas/station_schema.py

from pydantic import BaseModel
from typing import Optional

class StationBase(BaseModel):
    machine_group_id: int
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    user_id: int
    info: Optional[str] = None

class StationCreate(StationBase):
    pass

class StationUpdate(StationBase):
    pass

class StationResponse(StationBase):
    id: int

    class Config:
        orm_mode = True
