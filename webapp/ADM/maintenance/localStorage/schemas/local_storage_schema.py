# schemas/local_storage_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LocalStorageBase(BaseModel):
    key: str
    value: str

class LocalStorageCreate(LocalStorageBase):
    pass

class LocalStorageUpdate(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None

class LocalStorageResponse(LocalStorageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
