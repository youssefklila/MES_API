"""Report schema module."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ReportStatus(str, Enum):
    """Report status enum."""
    DONE = "done"
    PENDING = "pending"
    FAILED = "failed"

class ReportBase(BaseModel):
    """Base report schema."""
    report_text: str
    status: ReportStatus = ReportStatus.PENDING

class ReportCreate(ReportBase):
    """Report create schema."""
    pass

class ReportUpdate(BaseModel):
    """Report update schema."""
    report_text: Optional[str] = None
    status: Optional[ReportStatus] = None

class ReportResponse(ReportBase):
    """Report response schema."""
    id: int
    submitted_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True
