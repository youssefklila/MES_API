# services/line_service.py

from typing import List, Optional, Dict, Union
from datetime import datetime
from webapp.ADM.machine_assets.machine_setup.line.repositories.line_repository import LineRepository
from webapp.ADM.machine_assets.machine_setup.line.schemas.line_schema import (
    LineResponse, LineCreate, LineUpdate
)

class LineService:
    def __init__(self, repository: LineRepository):
        self.repository = repository

    def _to_response(self, line_dict: Dict) -> LineResponse:
        """Convert dictionary to Pydantic response model."""
        return LineResponse(**line_dict)

    def get_all_lines(self) -> List[LineResponse]:
        """Get all lines with their associated stations."""
        try:
            lines = self.repository.get_all()
            return [self._to_response(line) for line in lines]
        except Exception as e:
            raise ValueError(f"Failed to get lines: {str(e)}")

    def get_line_by_id(self, line_id: int) -> Optional[LineResponse]:
        """Get a line by ID with its associated stations."""
        try:
            line = self.repository.get_by_id(line_id)
            if line:
                return self._to_response(line)
            return None
        except Exception as e:
            raise ValueError(f"Failed to get line: {str(e)}")

    def get_lines_by_station_id(self, station_id: int) -> List[LineResponse]:
        """Get all lines that include the specified station."""
        try:
            lines = self.repository.get_by_station_id(station_id)
            return [self._to_response(line) for line in lines]
        except Exception as e:
            raise ValueError(f"Failed to get lines by station ID: {str(e)}")

    def add_line(self, line_data: Union[LineCreate, Dict]) -> LineResponse:
        """
        Add a new line with associated stations.
        
        Args:
            line_data: Either a LineCreate Pydantic model or a dictionary containing:
                - name: str (required)
                - description: Optional[str]
                - date: Optional[datetime]
                - station_ids: List[int] (required, at least one station ID)
                - user_id: Optional[int]
        """
        try:
            # Convert Pydantic model to dict if needed
            if hasattr(line_data, 'model_dump'):
                line_data = line_data.model_dump()
                
            # Extract and validate data
            name = line_data.get('name', '').strip()
            if not name:
                raise ValueError("Name is required")
                
            station_ids = line_data.get('station_ids', [])
            if not station_ids or not isinstance(station_ids, list) or not all(isinstance(x, int) for x in station_ids):
                raise ValueError("At least one valid station ID is required")
                
            user_id = line_data.get('user_id', 22)  # Default to 22 if not provided
            
            # Prepare data for repository
            line_kwargs = {
                'name': name,
                'description': line_data.get('description'),
                'date': line_data.get('date', datetime.utcnow()),
                'station_ids': station_ids,
                'user_id': user_id
            }
            
            # Remove None values
            line_kwargs = {k: v for k, v in line_kwargs.items() if v is not None}
            
            # Add the line
            line = self.repository.add(**line_kwargs)
            return self._to_response(line)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to create line: {str(e)}")

    def update_line(self, line_id: int, line_data: Union[LineUpdate, Dict]) -> Optional[LineResponse]:
        """
        Update a line and its associated stations.
        
        Args:
            line_id: ID of the line to update
            line_data: Either a LineUpdate Pydantic model or a dictionary containing:
                - name: Optional[str]
                - description: Optional[str]
                - date: Optional[datetime]
                - station_ids: Optional[List[int]]
                - user_id: Optional[int]
        """
        try:
            # Convert Pydantic model to dict if needed
            if hasattr(line_data, 'model_dump'):
                line_data = line_data.model_dump(exclude_unset=True)
                
            # Validate input
            if 'name' in line_data and (not line_data['name'] or not line_data['name'].strip()):
                raise ValueError("Name cannot be empty")
                
            if 'station_ids' in line_data and (
                not isinstance(line_data['station_ids'], list) or 
                not all(isinstance(x, int) for x in line_data['station_ids'])
            ):
                raise ValueError("station_ids must be a list of integers")
            
            # Update the line
            line = self.repository.update(line_id, **line_data)
            if line:
                return self._to_response(line)
            return None
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to update line: {str(e)}")

    def delete_line(self, line_id: int) -> bool:
        """
        Delete a line.
        
        Args:
            line_id: ID of the line to delete
            
        Returns:
            bool: True if the line was deleted, False if it didn't exist
        """
        try:
            # First check if the line exists
            line = self.repository.get_by_id(line_id)
            if not line:
                return False
                
            # If it exists, delete it
            return self.repository.delete_by_id(line_id)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to delete line: {str(e)}")
