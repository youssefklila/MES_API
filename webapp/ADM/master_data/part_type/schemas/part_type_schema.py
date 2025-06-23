# schemas/part_type_schema.py

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class PartTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: int
    is_active: Optional[bool] = True

class PartTypeCreate(PartTypeBase):
    pass

class PartTypeUpdate(PartTypeBase):
    pass

class PartTypeResponse(PartTypeBase):
    id: int
    date_of_creation: datetime
    date_of_change: datetime

    model_config = ConfigDict(from_attributes=True)
