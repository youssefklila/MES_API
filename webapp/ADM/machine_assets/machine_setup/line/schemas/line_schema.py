# schemas/line_schema.py

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class LineBase(BaseModel):
    name: str = Field(..., description="Name of the line")
    description: Optional[str] = Field(None, description="Description of the line")
    date: Optional[datetime] = Field(None, description="Date of the line")
    station_ids: List[int] = Field(default_factory=list, description="List of station IDs associated with this line")
    user_id: Optional[int] = Field(None, description="ID of the user who created this line")

class LineCreate(LineBase):
    """Schema for creating a Line."""
    pass

class LineUpdate(BaseModel):
    """Schema for updating a Line."""
    name: Optional[str] = Field(None, description="Name of the line")
    description: Optional[str] = Field(None, description="Description of the line")
    date: Optional[datetime] = Field(None, description="Date of the line")
    station_ids: Optional[List[int]] = Field(None, description="List of station IDs to associate with this line")
    user_id: Optional[int] = Field(None, description="ID of the user who updated this line")

class LineResponse(LineBase):
    """Schema for Line response."""
    id: int
    date: datetime
