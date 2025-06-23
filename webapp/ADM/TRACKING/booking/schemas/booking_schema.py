# schemas/booking_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookingBase(BaseModel):
    workorder_id: int
    station_id: int
    failed_id: int
    date_of_booking: datetime
    state: str
    mesure_id: Optional[int] = None

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    workorder_id: Optional[int] = None
    station_id: Optional[int] = None
    failed_id: Optional[int] = None
    date_of_booking: Optional[datetime] = None
    state: Optional[str] = None
    mesure_id: Optional[int] = None

class BookingResponse(BookingBase):
    id: int
    
    class Config:
        from_attributes = True
