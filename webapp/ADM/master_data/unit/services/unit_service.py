# services/unit_service.py

from typing import List, Optional, Dict

from webapp.ADM.master_data.unit.models.unit_model import Unit
from webapp.ADM.master_data.unit.repositories.unit_repository import UnitRepository
from webapp.ADM.master_data.unit.schemas.unit_schema import UnitResponse


class UnitService:
    def __init__(self, repository: UnitRepository):
        self.repository = repository

    def _to_response(self, unit_dict: Dict) -> UnitResponse:
        """Convert dictionary to Pydantic response model."""
        return UnitResponse(**unit_dict)

    def get_all_units(self) -> List[UnitResponse]:
        """Get all units."""
        try:
            units = self.repository.get_all()
            return [self._to_response(u) for u in units]
        except Exception as e:
            raise ValueError(f"Failed to get units: {str(e)}")

    def get_unit_by_id(self, unit_id: int) -> Optional[UnitResponse]:
        """Get a unit by ID."""
        try:
            unit = self.repository.get_by_id(unit_id)
            if unit:
                return self._to_response(unit)
            return None
        except Exception as e:
            raise ValueError(f"Failed to get unit: {str(e)}")

    def add_unit(self, unit_name: str, description: str) -> UnitResponse:
        """Add a new unit."""
        try:
            # Validate input
            if not unit_name or not unit_name.strip():
                raise ValueError("Unit name is required")
            
            unit = self.repository.add(unit_name.strip(), description)
            return self._to_response(unit)
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to create unit: {str(e)}")

    def update_unit(self, unit_id: int, **kwargs) -> Optional[UnitResponse]:
        """Update a unit."""
        try:
            # Validate input
            if 'unit_name' in kwargs and (not kwargs['unit_name'] or not kwargs['unit_name'].strip()):
                raise ValueError("Unit name cannot be empty")
            
            unit = self.repository.update_unit(unit_id, **kwargs)
            if unit:
                return self._to_response(unit)
            return None
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to update unit: {str(e)}")

    def delete_unit(self, unit_id: int) -> None:
        """Delete a unit."""
        try:
            self.repository.delete_by_id(unit_id)
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to delete unit: {str(e)}")
