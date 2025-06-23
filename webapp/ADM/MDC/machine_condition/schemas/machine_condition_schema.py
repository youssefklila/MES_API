"""Machine Condition schemas."""
from typing import Optional
from pydantic import BaseModel, Field


class MachineConditionBase(BaseModel):
    """Base schema for Machine Condition."""
    condition_name: str = Field(..., max_length=50, description="Name of the condition")
    condition_description: Optional[str] = Field(None, max_length=200, description="Description of the condition")
    color_rgb: Optional[str] = Field(None, max_length=20, description="RGB color value for the condition")
    is_active: Optional[bool] = Field(True, description="Whether the condition is active")


class MachineConditionCreate(MachineConditionBase):
    """Schema for creating a Machine Condition."""
    group_id: int = Field(..., description="ID of the parent Machine Condition Group")


class MachineConditionUpdate(BaseModel):
    """Schema for updating a Machine Condition."""
    condition_name: Optional[str] = Field(None, max_length=50, description="Name of the condition")
    condition_description: Optional[str] = Field(None, max_length=200, description="Description of the condition")
    color_rgb: Optional[str] = Field(None, max_length=20, description="RGB color value for the condition")
    group_id: Optional[int] = Field(None, description="ID of the parent Machine Condition Group")
    is_active: Optional[bool] = Field(None, description="Whether the condition is active")


class MachineConditionResponse(MachineConditionBase):
    """Schema for Machine Condition response."""
    id: int
    group_id: int

    class Config:
        """Pydantic config."""
        orm_mode = True
        from_attributes = True
