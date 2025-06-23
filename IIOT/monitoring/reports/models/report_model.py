"""Report model module."""

from sqlalchemy import Column, String, Integer, DateTime, Enum
from IIOT.database import Base
from datetime import datetime
import enum

class ReportStatus(str, enum.Enum):
    """Report status enum."""
    DONE = "done"
    PENDING = "pending"
    FAILED = "failed"

class Report(Base):
    """Report model class."""
    __tablename__ = "monitoring_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_text = Column(String, nullable=False)
    status = Column(Enum(ReportStatus), nullable=False, default=ReportStatus.PENDING)
    submitted_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Report(id={self.id}, " \
               f"status=\"{self.status}\", " \
               f"submitted_at=\"{self.submitted_at}\")>"
