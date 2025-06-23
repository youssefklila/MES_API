# endpoints/line_endpoint.py

from fastapi import APIRouter, Depends, HTTPException, Security, status
from typing import List, Dict, Any, Optional
from dependency_injector.wiring import inject, Provide

from webapp.ADM.machine_assets.machine_setup.line.schemas.line_schema import LineCreate, LineUpdate, LineResponse
from webapp.ADM.machine_assets.machine_setup.line.services.line_service import LineService
from webapp.containers import Container
from webapp.auth.dependencies import permission_required, oauth2_scheme

router = APIRouter(
    prefix="/lines",
    tags=["Lines"],
    responses={401: {"description": "Unauthorized"}, 403: {"description": "Forbidden"}}
)

# Permission constants
LINE_READ_PERM = "line:read"
LINE_CREATE_PERM = "line:create"
LINE_UPDATE_PERM = "line:update"
LINE_DELETE_PERM = "line:delete"

@router.get("/", response_model=List[LineResponse], summary="Get All Lines")
@inject
def get_lines(
    line_service: LineService = Depends(Provide[Container.line_service]),
    current_user: Dict[str, Any] = Depends(permission_required(LINE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all lines with their associated stations.
    
    Returns:
        List[LineResponse]: List of lines with their associated stations
        
    Requires line:read permission.
    """
    try:
        return line_service.get_all_lines()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving lines: {str(e)}"
        )

@router.get("/{line_id}", response_model=LineResponse, summary="Get Line by ID")
@inject
def get_line(
    line_id: int,
    line_service: LineService = Depends(Provide[Container.line_service]),
    current_user: Dict[str, Any] = Depends(permission_required(LINE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get a specific line by ID with its associated stations.
    
    Args:
        line_id: ID of the line to retrieve
        
    Returns:
        LineResponse: The requested line with its associated stations
        
    Raises:
        HTTPException: If the line is not found
        
    Requires line:read permission.
    """
    try:
        line = line_service.get_line_by_id(line_id)
        if not line:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Line with ID {line_id} not found"
            )
        return line
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving line: {str(e)}"
        )

@router.get("/station/{station_id}", response_model=List[LineResponse], summary="Get Lines by Station ID")
@inject
def get_lines_by_station(
    station_id: int,
    line_service: LineService = Depends(Provide[Container.line_service]),
    current_user: Dict[str, Any] = Depends(permission_required(LINE_READ_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Get all lines that include the specified station.
    
    Args:
        station_id: ID of the station to filter lines by
        
    Returns:
        List[LineResponse]: List of lines that include the specified station
        
    Requires line:read permission.
    """
    try:
        lines = line_service.get_lines_by_station_id(station_id)
        return lines
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving lines for station {station_id}: {str(e)}"
        )

@router.post("/", response_model=LineResponse, status_code=status.HTTP_201_CREATED, summary="Create Line")
@inject
def create_line(
    line_data: LineCreate,
    line_service: LineService = Depends(Provide[Container.line_service]),
    current_user: Dict[str, Any] = Depends(permission_required(LINE_CREATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Create a new line with associated stations.
    
    Args:
        line_data: Line creation data including station_ids
        
    Returns:
        LineResponse: The newly created line with associated stations
        
    Raises:
        HTTPException: If there's a validation error or the line cannot be created
        
    Requires line:create permission.
    """
    try:
        # Add the current user's ID to the line data if not provided
        line_dict = line_data.dict()
        if 'user_id' not in line_dict or not line_dict['user_id']:
            line_dict['user_id'] = current_user.get('id')
            
        # Create the line
        return line_service.add_line(line_dict)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating line: {str(e)}"
        )

@router.put("/{line_id}", response_model=LineResponse, summary="Update Line")
@inject
def update_line(
    line_id: int,
    line_data: LineUpdate,
    line_service: LineService = Depends(Provide[Container.line_service]),
    current_user: Dict[str, Any] = Depends(permission_required(LINE_UPDATE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Update a line and its associated stations.
    
    Args:
        line_id: ID of the line to update
        line_data: Line update data including optional station_ids
        
    Returns:
        LineResponse: The updated line with associated stations
        
    Raises:
        HTTPException: If the line is not found or there's a validation error
        
    Requires line:update permission.
    """
    try:
        # Update the line with the provided data
        line = line_service.update_line(line_id, line_data)
        if not line:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Line with ID {line_id} not found"
            )
        return line
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating line: {str(e)}"
        )

@router.delete("/{line_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Line")
@inject
def delete_line(
    line_id: int,
    line_service: LineService = Depends(Provide[Container.line_service]),
    current_user: Dict[str, Any] = Depends(permission_required(LINE_DELETE_PERM)),
    token: str = Security(oauth2_scheme)
):
    """
    Delete a line.
    
    Args:
        line_id: ID of the line to delete
        
    Raises:
        HTTPException: If the line is not found or cannot be deleted
        
    Requires line:delete permission.
    """
    try:
        success = line_service.delete_line(line_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Line with ID {line_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting line: {str(e)}"
        )
    return None
