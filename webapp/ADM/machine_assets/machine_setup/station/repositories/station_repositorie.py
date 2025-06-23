# repositories/station_repository.py

from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Callable, List, Dict, Any, Optional
from webapp.ADM.machine_assets.machine_setup.station.models.station_model import Station
from webapp.ADM.master_data.workorder.models.workorder_model import WorkOrder
from webapp.ADM.master_data.workplan_data.workplan.models.workplan_model import WorkPlan
from webapp.ADM.master_data.workplan_data.worksteps.models.workstep_model import WorkStep
from webapp.ADM.machine_assets.erp_group.erp.models.erp_model import ERPGroup
from webapp.ADM.machine_assets.erp_group.assign_station.models.assign_stations_to_erpgrp_model import AssignStationsToErpGrp
from webapp.ADM.machine_assets.machine_setup.line.models.line_model import Line, line_station_association

class StationRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            stations = session.query(Station).all()
            return [self._to_dict(station) for station in stations]

    def get_by_id(self, station_id: int) -> Optional[Dict[str, Any]]:
        with self.session_factory() as session:
            station = session.query(Station).filter(Station.id == station_id).first()
            if station:
                return self._to_dict(station)
            return None

    def add(self, machine_group_id: int, name: str, description: str, is_active: bool, user_id: int, info: str) -> Dict[str, Any]:
        with self.session_factory() as session:
            station = Station(
                machine_group_id=machine_group_id,
                name=name,
                description=description,
                is_active=is_active,
                user_id=user_id,
                info=info
            )
            session.add(station)
            session.commit()
            session.refresh(station)
            return self._to_dict(station)

    def delete_by_id(self, station_id: int) -> bool:
        with self.session_factory() as session:
            station = session.query(Station).filter(Station.id == station_id).first()
            if station:
                session.delete(station)
                session.commit()
                return True
            return False

    def update_station(self, station_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        with self.session_factory() as session:
            station = session.query(Station).filter(Station.id == station_id).first()
            if station:
                for key, value in kwargs.items():
                    setattr(station, key, value)
                session.commit()
                session.refresh(station)
                return self._to_dict(station)
            return None

    def get_by_line_name(self, line_name: str) -> List[Dict[str, Any]]:
        """
        Get all stations associated with a specific line name.
        
        Args:
            line_name: The name of the line to search for
            
        Returns:
            List of station dictionaries that are associated with the specified line name
        """
        with self.session_factory() as session:
            # Query stations that are associated with lines matching the given name
            # Using case-insensitive comparison and trimming whitespace
            stations = (
                session.query(Station)
                .join(
                    line_station_association,
                    Station.id == line_station_association.c.station_id
                )
                .join(
                    Line,
                    line_station_association.c.line_id == Line.id
                )
                .filter(
                    func.lower(func.trim(Line.name)) == func.lower(line_name.strip())
                )
                .distinct()
                .all()
            )
            
            return [self._to_dict(station) for station in stations]
    
    def _to_dict(self, station: Station) -> Dict[str, Any]:
        """Convert a station object to a dictionary."""
        return {
            "id": station.id,
            "machine_group_id": station.machine_group_id,
            "name": station.name,
            "description": station.description,
            "is_active": station.is_active,
            "user_id": station.user_id,
            "info": station.info
        }

    def get_workorders_by_station_id(self, station_id: int):
        with self.session_factory() as session:
            return (session.query(WorkOrder)
                    .join(WorkOrder.workplan)
                    .join(WorkPlan.work_steps)
                    .join(WorkStep.erp_group)
                    .join(AssignStationsToErpGrp, ERPGroup.id == AssignStationsToErpGrp.erp_group_id)
                    .filter(AssignStationsToErpGrp.station_id == station_id)
                    .all())
