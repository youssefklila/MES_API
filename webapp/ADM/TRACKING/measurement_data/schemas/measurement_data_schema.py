# schemas/measurement_data_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MeasurementDataBase(BaseModel):
    """Base schema for Measurement Data."""
    station_id: int = Field(..., description="Station ID")
    workorder_id: int = Field(..., description="Work Order ID")
    book_date: datetime = Field(..., description="Book Date")
    measure_name: str = Field(..., description="Measure Name", max_length=80)
    measure_value: str = Field(..., description="Measure Value", max_length=800)
    lower_limit: Optional[str] = Field(None, description="Lower Limit", max_length=30)
    upper_limit: Optional[str] = Field(None, description="Upper Limit", max_length=30)
    nominal: Optional[str] = Field(None, description="Nominal", max_length=50)
    tolerance: Optional[str] = Field(None, description="Tolerance", max_length=30)
    measure_fail_code: Optional[int] = Field(None, description="Measure Fail Code")
    booking_id: Optional[int] = Field(None, description="Booking ID")
    measure_type: Optional[str] = Field(None, description="Measure Type", max_length=20)

class MeasurementDataCreate(MeasurementDataBase):
    """Schema for creating a new Measurement Data."""
    pass

class MeasurementDataUpdate(BaseModel):
    """Schema for updating a Measurement Data."""
    station_id: Optional[int] = Field(None, description="Station ID")
    workorder_id: Optional[int] = Field(None, description="Work Order ID")
    book_date: Optional[datetime] = Field(None, description="Book Date")
    measure_name: Optional[str] = Field(None, description="Measure Name", max_length=80)
    measure_value: Optional[str] = Field(None, description="Measure Value", max_length=800)
    lower_limit: Optional[str] = Field(None, description="Lower Limit", max_length=30)
    upper_limit: Optional[str] = Field(None, description="Upper Limit", max_length=30)
    nominal: Optional[str] = Field(None, description="Nominal", max_length=50)
    tolerance: Optional[str] = Field(None, description="Tolerance", max_length=30)
    measure_fail_code: Optional[int] = Field(None, description="Measure Fail Code")
    booking_id: Optional[int] = Field(None, description="Booking ID")
    measure_type: Optional[str] = Field(None, description="Measure Type", max_length=20)

class MeasurementDataResponse(MeasurementDataBase):
    """Schema for Measurement Data response."""
    id: int = Field(..., description="Measurement Data ID")

    class Config:
        orm_mode = True
