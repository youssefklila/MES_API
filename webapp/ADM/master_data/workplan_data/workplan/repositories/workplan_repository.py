from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from typing import Callable, List

from webapp.ADM.master_data.workplan_data.workplan.models.workplan_model import WorkPlan


class WorkPlanRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> List[WorkPlan]:
        with self.session_factory() as session:
            return session.query(WorkPlan).all()

    def get_by_id(self, workplan_id: int) -> WorkPlan:
        with self.session_factory() as session:
            return session.query(WorkPlan).filter(WorkPlan.id == workplan_id).first()

    def add(self, **kwargs) -> WorkPlan:
        with self.session_factory() as session:
            workplan = WorkPlan(**kwargs)
            session.add(workplan)
            session.commit()
            session.refresh(workplan)
            return workplan

    def delete_by_id(self, workplan_id: int) -> bool:
        with self.session_factory() as session:
            work_plan = session.query(WorkPlan).filter(WorkPlan.id == workplan_id).first()
            if work_plan:
                session.delete(work_plan)
                session.commit()
                return True
            return False

    def update_work_plan(self, workplan_id: int, **kwargs) -> WorkPlan:
        with self.session_factory() as session:
            workplan = session.query(WorkPlan).filter(WorkPlan.id == workplan_id).first()
            if workplan:
                for key, value in kwargs.items():
                    setattr(workplan, key, value)
                session.commit()
                session.refresh(workplan)
            return workplan
