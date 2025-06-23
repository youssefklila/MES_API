# endpoints/measurement_data_endpoint.py

from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Security, status
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer

# Use deferred import to avoid circular imports
from webapp.ADM.TRACKING.measurement_data.services.measurement_data_service import MeasurementDataService
from webapp.ADM.TRACKING.measurement_data.schemas.measurement_data_schema import (
    MeasurementDataCreate,
    MeasurementDataResponse,
    MeasurementDataUpdate
)
from webapp.auth.dependencies import permission_required, oauth2_scheme

router = APIRouter(
    prefix="/measurement-data",
    tags=["measurement-data"],
    responses={404: {"description": "Not found"}},
)

# Permission constants
MEASUREMENT_DATA_READ_PERM = "measurement_data:read"
MEASUREMENT_DATA_CREATE_PERM = "measurement_data:create"
MEASUREMENT_DATA_UPDATE_PERM = "measurement_data:update"
MEASUREMENT_DATA_DELETE_PERM = "measurement_data:delete"

@router.get("/", response_model=List[MeasurementDataResponse], summary="Get All Measurement Data")
@inject
def get_all_measurement_data(
    service: MeasurementDataService = Depends(Provide["measurement_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(MEASUREMENT_DATA_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all measurement data.
    
    Requires measurement_data:read permission.
    """
    return service.get_all()

@router.get("/{measurement_id}", response_model=MeasurementDataResponse, summary="Get Measurement Data by ID")
@inject
def get_measurement_data_by_id(
    measurement_id: int,
    service: MeasurementDataService = Depends(Provide["measurement_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(MEASUREMENT_DATA_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific measurement data by ID.
    
    Requires measurement_data:read permission.
    """
    measurement_data = service.get_by_id(measurement_id)
    if not measurement_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Measurement data with ID {measurement_id} not found"
        )
    return measurement_data

@router.post("/", response_model=MeasurementDataResponse, status_code=status.HTTP_201_CREATED, summary="Create Measurement Data")
@inject
def create_measurement_data(
    measurement_data: MeasurementDataCreate,
    service: MeasurementDataService = Depends(Provide["measurement_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(MEASUREMENT_DATA_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new measurement data.
    
    Requires measurement_data:create permission.
    """
    # Add current user ID and timestamp
    measurement_data_dict = measurement_data.dict()
    measurement_data_dict["user_id"] = current_user.get("id")
    measurement_data_dict["created_at"] = datetime.now()
    # Remove keys not accepted by service.create
    measurement_data_dict.pop("user_id", None)
    measurement_data_dict.pop("created_at", None)
    
    return service.create(**measurement_data_dict)

@router.put("/{measurement_id}", response_model=MeasurementDataResponse, summary="Update Measurement Data")
@inject
def update_measurement_data(
    measurement_id: int,
    measurement_data: MeasurementDataUpdate,
    service: MeasurementDataService = Depends(Provide["measurement_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(MEASUREMENT_DATA_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a measurement data.
    
    Requires measurement_data:update permission.
    """
    existing_data = service.get_by_id(measurement_id)
    if not existing_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Measurement data with ID {measurement_id} not found"
        )
    
    return service.update(measurement_id, **measurement_data.dict(exclude_unset=True))

@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Measurement Data")
@inject
def delete_measurement_data(
    measurement_id: int,
    service: MeasurementDataService = Depends(Provide["measurement_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(MEASUREMENT_DATA_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a measurement data.
    
    Requires measurement_data:delete permission.
    """
    existing_data = service.get_by_id(measurement_id)
    if not existing_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Measurement data with ID {measurement_id} not found"
        )
    
    service.delete(measurement_id)
    return None

@router.get("/workorder/{workorder_id}", response_model=List[MeasurementDataResponse], summary="Get Measurement Data by Workorder ID")
@inject
def get_measurement_data_by_workorder(
    workorder_id: int,
    service: MeasurementDataService = Depends(Provide["measurement_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(MEASUREMENT_DATA_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all measurement data for a specific workorder.
    """
    return service.get_by_workorder_id(workorder_id)

@router.get("/station/{station_id}", response_model=List[MeasurementDataResponse], summary="Get Measurement Data by Station ID")
@inject
def get_measurement_data_by_station(
    station_id: int,
    service: MeasurementDataService = Depends(Provide["measurement_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(MEASUREMENT_DATA_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all measurement data for a specific station.
    """
    return service.get_by_station_id(station_id)

@router.get("/booking/{booking_id}", response_model=List[MeasurementDataResponse], summary="Get Measurement Data by Booking ID")
@inject
def get_measurement_data_by_booking(
    booking_id: int,
    service: MeasurementDataService = Depends(Provide["measurement_data_service"]),
    current_user: Dict[str, Any] = Depends(permission_required(MEASUREMENT_DATA_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all measurement data for a specific booking.
    """
    return service.get_by_booking_id(booking_id)
