# repositories/machine_group_repository.py

from typing import Dict, Any, List
from webapp.ADM.machine_assets.machine_setup.machine_group.models.machine_group_model import MachineGroup


class MachineGroupRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, name: str, description: str, user_id: int, cell_id: int, is_active: bool, failure: bool) -> Dict[str, Any]:
        with self.session_factory() as session:
            machine_group = MachineGroup(
                name=name,
                description=description,
                user_id=user_id,
                cell_id=cell_id,
                is_active=is_active,
                failure=failure
            )
            session.add(machine_group)
            session.commit()
            session.refresh(machine_group)
            return self._to_dict(machine_group)

    def get_by_id(self, machine_group_id: int) -> Dict[str, Any]:
        with self.session_factory() as session:
            machine_group = session.query(MachineGroup).filter(MachineGroup.id == machine_group_id).first()
            if machine_group:
                return self._to_dict(machine_group)
            return {}

    def get_all(self) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            machine_groups = session.query(MachineGroup).all()
            return [self._to_dict(mg) for mg in machine_groups]

    def update(self, machine_group_id: int, name: str, description: str, is_active: bool, failure: bool) -> Dict[str, Any]:
        with self.session_factory() as session:
            machine_group = session.query(MachineGroup).filter(MachineGroup.id == machine_group_id).first()
            if machine_group:
                machine_group.name = name
                machine_group.description = description
                machine_group.is_active = is_active
                machine_group.failure = failure
                session.commit()
                session.refresh(machine_group)
                return self._to_dict(machine_group)
            return {}

    def delete(self, machine_group_id: int) -> bool:
        with self.session_factory() as session:
            machine_group = session.query(MachineGroup).filter(MachineGroup.id == machine_group_id).first()
            if machine_group:
                # Check if there are any stations associated with this machine group
                if machine_group.stations:
                    # Cannot delete machine group with associated stations
                    return False
                session.delete(machine_group)
                session.commit()
                return True
            return False

    def _to_dict(self, machine_group: MachineGroup) -> Dict[str, Any]:
        """Convert a machine group object to a dictionary."""
        return {
            "id": machine_group.id,
            "name": machine_group.name,
            "description": machine_group.description,
            "user_id": machine_group.user_id,
            "cell_id": machine_group.cell_id,
            "is_active": machine_group.is_active,
            "failure": machine_group.failure
        }
