# repositories/cell_repository.py

from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from typing import Callable, List, Dict, Any

from webapp.ADM.machine_assets.machine_setup.cell.models.cell_model import Cell


class CellRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all cells."""
        with self.session_factory() as session:
            cells = session.query(Cell).all()
            return [self._to_dict(cell) for cell in cells]

    def get_by_id(self, cell_id: int) -> Dict[str, Any]:
        """Get a cell by ID."""
        with self.session_factory() as session:
            cell = session.query(Cell).filter(Cell.id == cell_id).first()
            if cell:
                return self._to_dict(cell)
            return {}

    def add(self, name: str, description: str, site_id: int, user_id: int, info: str, is_active: bool) -> Dict[str, Any]:
        """Add a new cell."""
        with self.session_factory() as session:
            cell = Cell(
                name=name,
                description=description,
                site_id=site_id,
                user_id=user_id,
                info=info,
                is_active=is_active
            )
            session.add(cell)
            session.commit()
            session.refresh(cell)
            return self._to_dict(cell)

    def delete_by_id(self, cell_id: int) -> None:
        """Delete a cell by ID."""
        with self.session_factory() as session:
            cell = session.query(Cell).filter(Cell.id == cell_id).first()
            if cell:
                session.delete(cell)
                session.commit()

    def update_cell(self, cell_id: int, **kwargs) -> Dict[str, Any]:
        """Update a cell."""
        with self.session_factory() as session:
            cell = session.query(Cell).filter(Cell.id == cell_id).first()
            if cell:
                for key, value in kwargs.items():
                    setattr(cell, key, value)
                session.commit()
                session.refresh(cell)
                return self._to_dict(cell)
            return {}

    def _to_dict(self, cell: Cell) -> Dict[str, Any]:
        """Convert a cell object to a dictionary."""
        return {
            "id": cell.id,
            "user_id": cell.user_id,
            "site_id": cell.site_id,
            "name": cell.name,
            "description": cell.description,
            "info": cell.info,
            "is_active": cell.is_active
        }
