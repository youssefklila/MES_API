"""Machine Condition Data schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MachineConditionDataBase(BaseModel):
    """Base schema for Machine Condition Data."""
    date_from: datetime = Field(..., description="Start date and time of the condition")
    date_to: Optional[datetime] = Field(None, description="End date and time of the condition")
    station_id: int = Field(..., description="ID of the station")
    condition_id: int = Field(..., description="ID of the machine condition")
    level: Optional[str] = Field(None, max_length=20, description="Level of the condition")
    condition_stamp: Optional[datetime] = Field(None, description="Timestamp of the condition")
    condition_type: Optional[str] = Field(None, max_length=1, description="Type of the condition")


class MachineConditionDataCreate(MachineConditionDataBase):
    """Schema for creating a Machine Condition Data."""
    pass


class MachineConditionDataUpdate(BaseModel):
    """Schema for updating a Machine Condition Data."""
    date_from: Optional[datetime] = Field(None, description="Start date and time of the condition")
    date_to: Optional[datetime] = Field(None, description="End date and time of the condition")
    station_id: Optional[int] = Field(None, description="ID of the station")
    condition_id: Optional[int] = Field(None, description="ID of the machine condition")
    level: Optional[str] = Field(None, max_length=20, description="Level of the condition")
    condition_stamp: Optional[datetime] = Field(None, description="Timestamp of the condition")
    condition_type: Optional[str] = Field(None, max_length=1, description="Type of the condition")


class MachineConditionDataResponse(MachineConditionDataBase):
    """Schema for Machine Condition Data response."""
    id: int
    condition_created: datetime

    class Config:
        """Pydantic config."""
        orm_mode = True
