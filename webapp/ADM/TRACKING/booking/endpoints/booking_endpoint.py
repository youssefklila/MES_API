# endpoints/booking_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security, status, Query
from typing import List, Dict, Any
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime

from webapp.ADM.TRACKING.booking.schemas.booking_schema import BookingCreate, BookingUpdate, BookingResponse
from webapp.ADM.TRACKING.booking.services.booking_service import BookingService
from webapp.containers import Container
from webapp.auth.dependencies import get_current_user, permission_required

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
BOOKING_READ_PERM = "booking:read"
BOOKING_CREATE_PERM = "booking:create"
BOOKING_UPDATE_PERM = "booking:update"
BOOKING_DELETE_PERM = "booking:delete"
BOOKING_STATS_PERM = "booking:read"  # Using read permission for statistics

@router.get("/", response_model=List[BookingResponse], summary="Get All Bookings")
@inject
def get_all_bookings(
    booking_service: BookingService = Depends(Provide[Container.booking_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOOKING_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all bookings.
    
    Requires booking:read permission.
    """
    return booking_service.get_all_bookings()

@router.get("/{booking_id}", response_model=BookingResponse, summary="Get Booking")
@inject
def get_booking(
    booking_id: int,
    booking_service: BookingService = Depends(Provide[Container.booking_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOOKING_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific booking by ID.
    
    Requires booking:read permission.
    """
    booking = booking_service.get_booking_by_id(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.post("/", response_model=BookingResponse, status_code=201, summary="Create Booking")
@inject
def create_booking(
    booking_data: BookingCreate,
    booking_service: BookingService = Depends(Provide[Container.booking_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOOKING_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new booking.
    
    Requires booking:create permission.
    """
    return booking_service.create_booking(**booking_data.dict())

@router.put("/{booking_id}", response_model=BookingResponse, summary="Update Booking")
@inject
def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    booking_service: BookingService = Depends(Provide[Container.booking_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOOKING_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a booking.
    
    Requires booking:update permission.
    """
    updated_booking = booking_service.update_booking(booking_id, **booking_data.dict(exclude_unset=True))
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking

@router.delete("/{booking_id}", status_code=204, summary="Delete Booking")
@inject
def delete_booking(
    booking_id: int,
    booking_service: BookingService = Depends(Provide[Container.booking_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOOKING_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a booking.
    
    Requires booking:delete permission.
    """
    success = booking_service.delete_booking(booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted successfully"}

@router.get("/statistics/states", response_model=Dict[str, int], summary="Get Booking State Statistics")
@inject
def get_state_statistics(
    booking_service: BookingService = Depends(Provide[Container.booking_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOOKING_STATS_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get statistics about the number of bookings per state.
    
    Returns a dictionary where keys are states and values are counts.
    
    Requires booking:read permission.
    """
    return booking_service.get_state_statistics()

@router.get("/search/state/{state}", response_model=List[BookingResponse], summary="Search Bookings By State")
@inject
def search_bookings_by_state(
    state: str,
    booking_service: BookingService = Depends(Provide[Container.booking_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOOKING_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Search for bookings by state.
    
    Requires booking:read permission.
    """
    bookings = booking_service.search_bookings_by_state(state)
    return bookings

@router.get("/search/date-range/", response_model=List[BookingResponse], summary="Get Bookings By Date Range")
@inject
def get_bookings_by_date_range(
    start_date: datetime = Query(..., description="Start date (inclusive) in ISO format"),
    end_date: datetime = Query(..., description="End date (inclusive) in ISO format"),
    booking_service: BookingService = Depends(Provide[Container.booking_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOOKING_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all bookings within a specific date range.
    
    - **start_date**: Start date (inclusive) in ISO format (YYYY-MM-DDTHH:MM:SS)
    - **end_date**: End date (inclusive) in ISO format (YYYY-MM-DDTHH:MM:SS)
    
    Requires booking:read permission.
    """
    try:
        bookings = booking_service.get_bookings_by_date_range(start_date, end_date)
        return bookings
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/search/state-date/", response_model=List[BookingResponse], summary="Get Bookings By State And Date Range")
@inject
def get_bookings_by_state_and_date(
    state: str = Query(..., description="Booking state to filter by"),
    start_date: datetime = Query(..., description="Start date (inclusive) in ISO format"),
    end_date: datetime = Query(..., description="End date (inclusive) in ISO format"),
    booking_service: BookingService = Depends(Provide[Container.booking_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOOKING_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all bookings with a specific state and within a date range.
    
    - **state**: Booking state to filter by
    - **start_date**: Start date (inclusive) in ISO format (YYYY-MM-DDTHH:MM:SS)
    - **end_date**: End date (inclusive) in ISO format (YYYY-MM-DDTHH:MM:SS)
    
    Requires booking:read permission.
    """
    try:
        bookings = booking_service.get_bookings_by_state_and_date(state, start_date, end_date)
        return bookings
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/search/workorder/{workorder_id}", response_model=List[BookingResponse], summary="Get Bookings By Workorder ID")
@inject
def get_bookings_by_workorder_id(
    workorder_id: int,
    booking_service: BookingService = Depends(Provide[Container.booking_service]),
    current_user: Dict[str, Any] = Depends(permission_required(BOOKING_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all bookings associated with a specific workorder.
    
    - **workorder_id**: ID of the workorder to filter by
    
    Requires booking:read permission.
    """
    try:
        bookings = booking_service.get_bookings_by_workorder_id(workorder_id)
        return bookings
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
