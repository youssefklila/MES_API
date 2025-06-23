"""Machine Condition Group schemas."""
from pydantic import BaseModel, Field
from typing import Optional


class MachineConditionGroupBase(BaseModel):
    """Base schema for Machine Condition Group."""
    
    group_name: str = Field(..., max_length=50, description="Name of the machine condition group")
    group_description: Optional[str] = Field(None, max_length=200, description="Description of the machine condition group")
    # color_rgb field has been moved to machine_condition schema
    is_active: Optional[bool] = Field(True, description="Whether the machine condition group is active")


class MachineConditionGroupCreate(MachineConditionGroupBase):
    """Schema for creating a Machine Condition Group."""
    pass


class MachineConditionGroupUpdate(MachineConditionGroupBase):
    """Schema for updating a Machine Condition Group."""
    group_name: Optional[str] = Field(None, max_length=50, description="Name of the machine condition group")


class MachineConditionGroupResponse(MachineConditionGroupBase):
    """Schema for Machine Condition Group response."""
    
    id: int = Field(..., description="ID of the machine condition group")

    class Config:
        """Pydantic config."""
        
        orm_mode = True
        from_attributes = True
