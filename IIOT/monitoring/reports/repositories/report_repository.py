"""Report repository module."""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from IIOT.monitoring.reports.models.report_model import Report, ReportStatus

class ReportNotFoundError(Exception):
    """Report not found error."""
    pass

class ReportRepository:
    """Report repository class."""

    def __init__(self, session_factory):
        """Initialize report repository."""
        self._session_factory = session_factory

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all reports as dictionaries."""
        with self._session_factory() as session:
            reports = session.query(Report).all()
            return [
                {
                    "id": report.id,
                    "report_text": report.report_text,
                    "status": report.status,
                    "submitted_at": report.submitted_at
                }
                for report in reports
            ]

    def get_by_id(self, report_id: int) -> Dict[str, Any]:
        """Get report by ID as dictionary."""
        with self._session_factory() as session:
            report = session.query(Report).get(report_id)
            if report is None:
                raise ReportNotFoundError(f"Report with ID {report_id} not found")
            return {
                "id": report.id,
                "report_text": report.report_text,
                "status": report.status,
                "submitted_at": report.submitted_at
            }

    def add(self, report_text: str, status: ReportStatus = ReportStatus.PENDING) -> Dict[str, Any]:
        """Add a new report and return as dictionary."""
        with self._session_factory() as session:
            # Ensure status is a ReportStatus enum value
            if not isinstance(status, ReportStatus):
                status = ReportStatus(status)
            
            report = Report(
                report_text=report_text,
                status=status
            )
            session.add(report)
            session.commit()
            session.refresh(report)
            return {
                "id": report.id,
                "report_text": report.report_text,
                "status": report.status,
                "submitted_at": report.submitted_at
            }

    def update(self, report_id: int, **kwargs) -> Dict[str, Any]:
        """Update report and return as dictionary."""
        with self._session_factory() as session:
            report = session.query(Report).get(report_id)
            if report is None:
                raise ReportNotFoundError(f"Report with ID {report_id} not found")
            
            for key, value in kwargs.items():
                setattr(report, key, value)
            
            session.commit()
            session.refresh(report)
            return {
                "id": report.id,
                "report_text": report.report_text,
                "status": report.status,
                "submitted_at": report.submitted_at
            }

    def delete(self, report_id: int) -> None:
        """Delete report by ID."""
        with self._session_factory() as session:
            report = session.query(Report).get(report_id)
            if report is None:
                raise ReportNotFoundError(f"Report with ID {report_id} not found")
            session.delete(report)
            session.commit()
