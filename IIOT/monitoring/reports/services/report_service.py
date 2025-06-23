"""Report service module."""
from typing import List, Dict, Any
from IIOT.monitoring.reports.repositories.report_repository import ReportRepository
from IIOT.monitoring.reports.models.report_model import ReportStatus

class ReportService:
    """Report service class."""

    def __init__(self, report_repository: ReportRepository):
        """Initialize report service."""
        self._repository = report_repository

    def get_all_reports(self) -> List[Dict[str, Any]]:
        """Get all reports."""
        return self._repository.get_all()

    def get_report_by_id(self, report_id: int) -> Dict[str, Any]:
        """Get report by ID."""
        return self._repository.get_by_id(report_id)

    def create_report(self, report_text: str, status: ReportStatus = ReportStatus.PENDING) -> Dict[str, Any]:
        """Create a new report."""
        return self._repository.add(report_text, status)

    def update_report(self, report_id: int, **kwargs) -> Dict[str, Any]:
        """Update report."""
        return self._repository.update(report_id, **kwargs)

    def delete_report(self, report_id: int) -> None:
        """Delete report."""
        self._repository.delete(report_id)
