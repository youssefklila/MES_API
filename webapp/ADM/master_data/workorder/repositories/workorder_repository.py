from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from typing import Callable, List, Optional

from webapp.ADM.master_data.workorder.models.workorder_model import WorkOrder


class WorkOrderRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> List[WorkOrder]:
        with self.session_factory() as session:
            return session.query(WorkOrder).all()

    def get_by_id(self, workorder_id: int) -> Optional[WorkOrder]:
        with self.session_factory() as session:
            return session.query(WorkOrder).filter(WorkOrder.id == workorder_id).first()
            
    def get_by_workorder_no(self, workorder_no: str) -> Optional[WorkOrder]:
        with self.session_factory() as session:
            return session.query(WorkOrder).filter(WorkOrder.workorder_no == workorder_no).first()
            
    def get_by_part_number(self, part_number: str) -> List[WorkOrder]:
        with self.session_factory() as session:
            return session.query(WorkOrder).filter(WorkOrder.part_number == part_number).all()

    def add(self, **kwargs) -> WorkOrder:
        with self.session_factory() as session:
            workorder = WorkOrder(**kwargs)
            session.add(workorder)
            session.commit()
            session.refresh(workorder)
            return workorder

    def delete_by_id(self, workorder_id: int) -> bool:
        with self.session_factory() as session:
            workorder = session.query(WorkOrder).filter(WorkOrder.id == workorder_id).first()
            if workorder:
                session.delete(workorder)
                session.commit()
                return True
            return False

    def update(self, workorder_id: int, **kwargs) -> Optional[WorkOrder]:
        with self.session_factory() as session:
            workorder = session.query(WorkOrder).filter(WorkOrder.id == workorder_id).first()
            if workorder:
                for key, value in kwargs.items():
                    setattr(workorder, key, value)
                session.commit()
                session.refresh(workorder)
                return workorder
            return None
