# services/cell_service.py

from typing import List, Dict, Any, Optional

from webapp.ADM.machine_assets.machine_setup.cell.models.cell_model import Cell
from webapp.ADM.machine_assets.machine_setup.cell.repositories.cell_repositorie import CellRepository
from webapp.ADM.machine_assets.machine_setup.cell.schemas.cell_schema import CellResponse, CellCreate, CellUpdate


class CellService:
    def __init__(self, cell_repository: CellRepository) -> None:
        self.cell_repository = cell_repository

    def get_cells(self) -> List[CellResponse]:
        """Get all cells."""
        cells = self.cell_repository.get_all()
        return [CellResponse(**cell) for cell in cells]

    def get_cell_by_id(self, cell_id: int) -> Optional[CellResponse]:
        """Get a cell by ID."""
        cell = self.cell_repository.get_by_id(cell_id)
        if cell:
            return CellResponse(**cell)
        return None

    def create_cell(
        self,
        user_id: int,
        site_id: int,
        name: str,
        description: Optional[str] = None,
        info: Optional[Dict[str, Any]] = None,
        is_active: bool = True
    ) -> CellResponse:
        """Create a new cell."""
        # Convert info to string before creating the cell
        info_str = str(info) if info else ""
        cell = self.cell_repository.add(
            name=name,
            description=description or "",
            site_id=site_id,
            user_id=user_id,
            info=info_str,
            is_active=is_active
        )
        return CellResponse(**cell)

    def update_cell(
        self,
        cell_id: int,
        user_id: int,
        site_id: int,
        name: str,
        description: Optional[str] = None,
        info: Optional[Dict[str, Any]] = None,
        is_active: bool = True
    ) -> Optional[CellResponse]:
        """Update a cell."""
        # Convert info to string before updating the cell
        info_str = str(info) if info else ""
        cell = self.cell_repository.update_cell(
            cell_id=cell_id,
            user_id=user_id,
            site_id=site_id,
            name=name,
            description=description or "",
            info=info_str,
            is_active=is_active
        )
        if cell:
            return CellResponse(**cell)
        return None

    def delete_cell_by_id(self, cell_id: int) -> bool:
        """Delete a cell by ID."""
        self.cell_repository.delete_by_id(cell_id)
        return True

    def _to_response(self, cell: Any) -> CellResponse:
        """Convert a cell object to a response model."""
        # Create response with the cell's attributes
        return CellResponse(
            id=cell.id,
            user_id=cell.user_id,
            site_id=cell.site_id,
            name=cell.name,
            description=cell.description,
            info=cell.info,
            is_active=cell.is_active
        )
