"""Active Workorder repository."""
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from typing import Callable, List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError

from webapp.ADM.master_data.active_workorder.models.active_workorder_model import ActiveWorkorder


class ActiveWorkorderRepository:
    """Repository for Active Workorder operations."""

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        """Initialize repository with session factory."""
        self.session_factory = session_factory
    
    def _to_dict(self, active_workorder: ActiveWorkorder) -> Dict[str, Any]:
        """Convert ActiveWorkorder model to dictionary."""
        return {
            "id": active_workorder.id,
            "workorder_id": active_workorder.workorder_id,
            "station_id": active_workorder.station_id,
            "state": active_workorder.state
        }

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all active workorders."""
        with self.session_factory() as session:
            active_workorders = session.query(ActiveWorkorder).all()
            return [self._to_dict(active_workorder) for active_workorder in active_workorders]

    def get_by_id(self, active_workorder_id: int) -> Optional[Dict[str, Any]]:
        """Get active workorder by ID."""
        with self.session_factory() as session:
            active_workorder = session.query(ActiveWorkorder).filter(ActiveWorkorder.id == active_workorder_id).first()
            if active_workorder:
                return self._to_dict(active_workorder)
            return None

    def get_by_workorder_id(self, workorder_id: int) -> List[Dict[str, Any]]:
        """Get active workorders by workorder ID."""
        with self.session_factory() as session:
            active_workorders = session.query(ActiveWorkorder).filter(ActiveWorkorder.workorder_id == workorder_id).all()
            return [self._to_dict(active_workorder) for active_workorder in active_workorders]

    def get_by_station_id(self, station_id: int) -> List[Dict[str, Any]]:
        """Get active workorders by station ID."""
        with self.session_factory() as session:
            active_workorders = session.query(ActiveWorkorder).filter(ActiveWorkorder.station_id == station_id).all()
            return [self._to_dict(active_workorder) for active_workorder in active_workorders]

    def get_by_state(self, state: int) -> List[Dict[str, Any]]:
        """Get active workorders by state."""
        with self.session_factory() as session:
            active_workorders = session.query(ActiveWorkorder).filter(ActiveWorkorder.state == state).all()
            return [self._to_dict(active_workorder) for active_workorder in active_workorders]

    def add(self, workorder_id: int, station_id: int, state: int) -> Dict[str, Any]:
        """Add new active workorder."""
        with self.session_factory() as session:
            try:
                active_workorder = ActiveWorkorder(
                    workorder_id=workorder_id,
                    station_id=station_id,
                    state=state
                )
                session.add(active_workorder)
                session.commit()
                session.refresh(active_workorder)
                return self._to_dict(active_workorder)
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def update(self, active_workorder_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update active workorder."""
        with self.session_factory() as session:
            try:
                active_workorder = session.query(ActiveWorkorder).filter(ActiveWorkorder.id == active_workorder_id).first()
                if not active_workorder:
                    return None

                for key, value in kwargs.items():
                    if hasattr(active_workorder, key) and value is not None:
                        setattr(active_workorder, key, value)

                session.commit()
                session.refresh(active_workorder)
                return self._to_dict(active_workorder)
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def delete(self, active_workorder_id: int) -> bool:
        """Delete active workorder."""
        with self.session_factory() as session:
            try:
                active_workorder = session.query(ActiveWorkorder).filter(ActiveWorkorder.id == active_workorder_id).first()
                if not active_workorder:
                    return False

                session.delete(active_workorder)
                session.commit()
                return True
            except SQLAlchemyError as e:
                session.rollback()
                raise e
