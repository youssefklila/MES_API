from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from typing import Callable, List, Optional

from webapp.ADM.master_data.workplan_data.worksteps.models.workstep_model import WorkStep


class WorkStepRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> List[WorkStep]:
        with self.session_factory() as session:
            return session.query(WorkStep).all()
            
    def get_by_workplan_id(self, workplan_id: int) -> List[WorkStep]:
        with self.session_factory() as session:
            return session.query(WorkStep).filter(WorkStep.workplan_id == workplan_id).all()

    def get_by_id(self, workstep_id: int) -> Optional[WorkStep]:
        with self.session_factory() as session:
            return session.query(WorkStep).filter(WorkStep.id == workstep_id).first()

    def add(self, **kwargs) -> WorkStep:
        with self.session_factory() as session:
            workstep = WorkStep(**kwargs)
            session.add(workstep)
            session.commit()
            session.refresh(workstep)
            return workstep

    def delete_by_id(self, workstep_id: int) -> bool:
        with self.session_factory() as session:
            workstep = session.query(WorkStep).filter(WorkStep.id == workstep_id).first()
            if workstep:
                session.delete(workstep)
                session.commit()
                return True
            return False

    def update_workstep(self, workstep_id: int, **kwargs) -> Optional[WorkStep]:
        with self.session_factory() as session:
            workstep = session.query(WorkStep).filter(WorkStep.id == workstep_id).first()
            if workstep:
                for key, value in kwargs.items():
                    setattr(workstep, key, value)
                session.commit()
                session.refresh(workstep)
                return workstep
            return None
