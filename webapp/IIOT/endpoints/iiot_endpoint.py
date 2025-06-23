"""IIOT Sensor Data endpoints."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Security, HTTPException, Query
from dependency_injector.wiring import inject, Provide

from webapp.IIOT.schemas.iiot_schema import (
    IIOTSensorDataCreate,
    IIOTSensorDataUpdate,
    IIOTSensorDataResponse
)
from webapp.IIOT.services.iiot_service import IIOTSensorDataService
from webapp.auth.dependencies import oauth2_scheme, permission_required

router = APIRouter(
    prefix="/iiot-sensor-data",
    tags=["IIOT"]  
)

# Permission constants
IIOT_SENSOR_DATA_READ_PERM = "iiot_sensor_data:read"
IIOT_SENSOR_DATA_CREATE_PERM = "iiot_sensor_data:create"
IIOT_SENSOR_DATA_UPDATE_PERM = "iiot_sensor_data:update"
IIOT_SENSOR_DATA_DELETE_PERM = "iiot_sensor_data:delete"

@router.get("/", response_model=List[IIOTSensorDataResponse], summary="Get All IIOT Sensor Data")
@inject
def get_all_sensor_data(
    service: IIOTSensorDataService = Depends(Provide["iiot_sensor_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(IIOT_SENSOR_DATA_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all IIOT sensor data.
    
    Requires iiot_sensor_data:read permission.
    """
    return service.get_all()

@router.get("/{sensor_data_id}", response_model=IIOTSensorDataResponse, summary="Get IIOT Sensor Data by ID")
@inject
def get_sensor_data_by_id(
    sensor_data_id: int,
    service: IIOTSensorDataService = Depends(Provide["iiot_sensor_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(IIOT_SENSOR_DATA_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific IIOT sensor data by ID.
    
    Requires iiot_sensor_data:read permission.
    """
    return service.get_by_id(sensor_data_id)

@router.get("/date-range/", response_model=List[IIOTSensorDataResponse], summary="Get IIOT Sensor Data by Date Range")
@inject
def get_sensor_data_by_date_range(
    start_date: datetime = Query(..., description="Start date (inclusive) in ISO format"),
    end_date: datetime = Query(..., description="End date (inclusive) in ISO format"),
    service: IIOTSensorDataService = Depends(Provide["iiot_sensor_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(IIOT_SENSOR_DATA_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all IIOT sensor data within a specific date range.
    
    - **start_date**: Start date (inclusive) in ISO format (YYYY-MM-DDTHH:MM:SS)
    - **end_date**: End date (inclusive) in ISO format (YYYY-MM-DDTHH:MM:SS)
    
    Requires iiot_sensor_data:read permission.
    """
    return service.get_by_date_range(start_date, end_date)

@router.post("/", response_model=IIOTSensorDataResponse, summary="Create IIOT Sensor Data")
@inject
def create_sensor_data(
    data: IIOTSensorDataCreate,
    service: IIOTSensorDataService = Depends(Provide["iiot_sensor_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(IIOT_SENSOR_DATA_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create new IIOT sensor data.
    
    Requires iiot_sensor_data:create permission.
    """
    return service.create_sensor_data(
        value=data.value,
        date=data.date,
        station_id=data.station_id
    )

@router.put("/{sensor_data_id}", response_model=IIOTSensorDataResponse, summary="Update IIOT Sensor Data")
@inject
def update_sensor_data(
    sensor_data_id: int,
    data: IIOTSensorDataUpdate,
    service: IIOTSensorDataService = Depends(Provide["iiot_sensor_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(IIOT_SENSOR_DATA_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update IIOT sensor data.
    
    Requires iiot_sensor_data:update permission.
    """
    update_data = data.dict(exclude_unset=True)
    return service.update_sensor_data(sensor_data_id, **update_data)

@router.delete("/{sensor_data_id}", response_model=Dict[str, str], summary="Delete IIOT Sensor Data")
@inject
def delete_sensor_data(
    sensor_data_id: int,
    service: IIOTSensorDataService = Depends(Provide["iiot_sensor_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(IIOT_SENSOR_DATA_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete IIOT sensor data.
    
    Requires iiot_sensor_data:delete permission.
    """
    service.delete_sensor_data(sensor_data_id)
    return {"message": "IIOT sensor data deleted successfully"}
