from typing import List, Optional

from webapp.ADM.master_data.workorder.models.workorder_model import WorkOrder
from webapp.ADM.master_data.workorder.repositories.workorder_repository import WorkOrderRepository


class WorkOrderService:
    def __init__(self, repository: WorkOrderRepository):
        self.repository = repository

    def get_all_workorders(self) -> List[WorkOrder]:
        return self.repository.get_all()

    def get_workorder_by_id(self, workorder_id: int) -> Optional[WorkOrder]:
        return self.repository.get_by_id(workorder_id)
        
    def get_workorder_by_workorder_no(self, workorder_no: str) -> Optional[WorkOrder]:
        return self.repository.get_by_workorder_no(workorder_no)
        
    def get_workorders_by_part_number(self, part_number: str) -> List[WorkOrder]:
        return self.repository.get_by_part_number(part_number)

    def add_workorder(self, **kwargs) -> WorkOrder:
        return self.repository.add(**kwargs)

    def delete_workorder(self, workorder_id: int) -> bool:
        return self.repository.delete_by_id(workorder_id)

    def update_workorder(self, workorder_id: int, **kwargs) -> Optional[WorkOrder]:
        return self.repository.update(workorder_id, **kwargs)
