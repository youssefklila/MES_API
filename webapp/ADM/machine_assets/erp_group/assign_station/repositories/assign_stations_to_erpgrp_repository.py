# repositories/assign_stations_to_erpgrp_repository.py

from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from typing import Callable, List, Dict, Any, Optional
from webapp.ADM.machine_assets.erp_group.assign_station.models.assign_stations_to_erpgrp_model import AssignStationsToErpGrp

class AssignStationsToErpGrpRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            assignments = session.query(AssignStationsToErpGrp).all()
            return [self._to_dict(assignment) for assignment in assignments]

    def get_by_id(self, assign_id: int) -> Optional[Dict[str, Any]]:
        with self.session_factory() as session:
            assignment = session.query(AssignStationsToErpGrp).filter(AssignStationsToErpGrp.id == assign_id).first()
            if assignment:
                return self._to_dict(assignment)
            return None

    def get_by_station_id(self, station_id: int) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            assignments = session.query(AssignStationsToErpGrp).filter(AssignStationsToErpGrp.station_id == station_id).all()
            return [self._to_dict(assignment) for assignment in assignments]

    def add(self, station_id: int, erp_group_id: int, station_type: str, user_id: int) -> Dict[str, Any]:
        with self.session_factory() as session:
            assign_st_erpgrp = AssignStationsToErpGrp(
                station_id=station_id,
                erp_group_id=erp_group_id,
                station_type=station_type,
                user_id=user_id
            )
            session.add(assign_st_erpgrp)
            session.commit()
            session.refresh(assign_st_erpgrp)
            return self._to_dict(assign_st_erpgrp)

    def delete_by_id(self, assign_id: int) -> bool:
        with self.session_factory() as session:
            assign_st_erpgrp = session.query(AssignStationsToErpGrp).filter(AssignStationsToErpGrp.id == assign_id).first()
            if assign_st_erpgrp:
                session.delete(assign_st_erpgrp)
                session.commit()
                return True
            return False

    def _to_dict(self, assignment: AssignStationsToErpGrp) -> Dict[str, Any]:
        """Convert an assignment object to a dictionary."""
        return {
            "id": assignment.id,
            "station_id": assignment.station_id,
            "erp_group_id": assignment.erp_group_id,
            "station_type": assignment.station_type,
            "user_id": assignment.user_id
        }
