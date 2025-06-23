"""Report endpoints module."""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from dependency_injector.wiring import inject, Provide
from typing import List, Dict, Any, Optional

from IIOT.containers import Container
from IIOT.monitoring.reports.schemas import ReportCreate, ReportUpdate, ReportResponse
from IIOT.monitoring.reports.services.report_service import ReportService
from IIOT.monitoring.reports.repositories.report_repository import ReportNotFoundError
from IIOT.auth.dependencies import get_current_user, permission_required

router = APIRouter(tags=["Reports"], prefix="/monitoring/reports")

# Permission constants
REPORT_READ_PERM = "report:read"
REPORT_CREATE_PERM = "report:create"
REPORT_UPDATE_PERM = "report:update"
REPORT_DELETE_PERM = "report:delete"

@router.get("/", response_model=List[ReportResponse])
@inject
async def get_all_reports(
    report_service: ReportService = Depends(Provide[Container.report_service]),
    current_user: Dict[str, Any] = Depends(permission_required(REPORT_READ_PERM))
):
    """Get all reports (requires report:read permission)."""
    try:
        return report_service.get_all_reports()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{report_id}", response_model=ReportResponse)
@inject
async def get_report_by_id(
    report_id: int,
    report_service: ReportService = Depends(Provide[Container.report_service]),
    current_user: Dict[str, Any] = Depends(permission_required(REPORT_READ_PERM))
):
    """Get report by ID (requires report:read permission)."""
    try:
        return report_service.get_report_by_id(report_id)
    except ReportNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_report(
    report_data: ReportCreate,
    report_service: ReportService = Depends(Provide[Container.report_service]),
    current_user: Dict[str, Any] = Depends(permission_required(REPORT_CREATE_PERM))
):
    """Create a new report (requires report:create permission)."""
    try:
        return report_service.create_report(
            report_text=report_data.report_text,
            status=report_data.status
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/{report_id}", response_model=ReportResponse)
@inject
async def update_report(
    report_id: int,
    report_data: ReportUpdate,
    report_service: ReportService = Depends(Provide[Container.report_service]),
    current_user: Dict[str, Any] = Depends(permission_required(REPORT_UPDATE_PERM))
):
    """Update report (requires report:update permission)."""
    try:
        # Create kwargs for the update method
        update_data = {}
        if report_data.report_text is not None:
            update_data["report_text"] = report_data.report_text
        if report_data.status is not None:
            update_data["status"] = report_data.status

        return report_service.update_report(report_id, **update_data)
    except ReportNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_report(
    report_id: int,
    report_service: ReportService = Depends(Provide[Container.report_service]),
    current_user: Dict[str, Any] = Depends(permission_required(REPORT_DELETE_PERM))
):
    """Delete report (requires report:delete permission)."""
    try:
        report_service.delete_report(report_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ReportNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
