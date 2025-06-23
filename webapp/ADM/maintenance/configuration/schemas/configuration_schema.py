# schemas/configuration_schema.py

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime
from enum import Enum

class ConfigurationState(str, Enum):
    ACTIVE = "ACTIVE"
    NOT_ACTIVE = "NOT_ACTIVE"

class ConfigurationBase(BaseModel):
    name: str
    description: Optional[str] = None
    url: str
    port: Optional[str] = None
    refresh_time: int = Field(..., description="Refresh time in seconds")
    state: ConfigurationState = ConfigurationState.ACTIVE
    station_id: Optional[int] = None

class ConfigurationCreate(ConfigurationBase):
    pass

class ConfigurationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    port: Optional[str] = None
    refresh_time: Optional[int] = None
    state: Optional[ConfigurationState] = None
    action_date: Optional[datetime] = None
    station_id: Optional[int] = None

class ConfigurationResponse(ConfigurationBase):
    id: int
    action_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
