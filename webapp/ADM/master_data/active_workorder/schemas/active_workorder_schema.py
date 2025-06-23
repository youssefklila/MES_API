"""Active Workorder schemas."""
from pydantic import BaseModel, Field, validator
from typing import Optional


class ActiveWorkorderBase(BaseModel):
    """Base schema for Active Workorder."""
    workorder_id: int = Field(..., description="ID of the workorder")
    station_id: int = Field(..., description="ID of the station")
    state: int = Field(..., description="State of the active workorder (0 to 5)")
    
    @validator('state')
    def validate_state(cls, v):
        """Validate that state is either 0, 1, 2, 3, 4, or 5."""
        if v not in [0, 1, 2, 3, 4, 5]:
            raise ValueError('State must be either 0, 1, 2, 3, 4, or 5')
        return v


class ActiveWorkorderCreate(ActiveWorkorderBase):
    """Schema for creating an Active Workorder."""
    pass


class ActiveWorkorderUpdate(BaseModel):
    """Schema for updating an Active Workorder."""
    workorder_id: Optional[int] = Field(None, description="ID of the workorder")
    station_id: Optional[int] = Field(None, description="ID of the station")
    state: Optional[int] = Field(None, description="State of the active workorder (0 to 5)")
    
    @validator('state')
    def validate_state(cls, v):
        """Validate that state is either 0, 1, 2, 3, 4, or 5."""
        if v is not None and v not in [0, 1, 2, 3, 4, 5]:
            raise ValueError('State must be either 0, 1, 2, 3, 4, or 5')
        return v


class ActiveWorkorderResponse(ActiveWorkorderBase):
    """Schema for Active Workorder response."""
    id: int = Field(..., description="ID of the active workorder")

    class Config:
        """Pydantic config."""
        from_attributes = True
