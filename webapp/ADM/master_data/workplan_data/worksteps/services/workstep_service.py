from typing import List, Optional

from webapp.ADM.master_data.workplan_data.worksteps.models.workstep_model import WorkStep
from webapp.ADM.master_data.workplan_data.worksteps.repositories.workstep_repository import WorkStepRepository


class WorkStepService:
    def __init__(self, repository: WorkStepRepository):
        self.repository = repository

    def get_all_worksteps(self) -> List[WorkStep]:
        return self.repository.get_all()
        
    def get_worksteps_by_workplan_id(self, workplan_id: int) -> List[WorkStep]:
        return self.repository.get_by_workplan_id(workplan_id)

    def get_workstep_by_id(self, workstep_id: int) -> Optional[WorkStep]:
        return self.repository.get_by_id(workstep_id)

    def add_workstep(self, **kwargs) -> WorkStep:
        return self.repository.add(**kwargs)

    def delete_workstep(self, workstep_id: int) -> bool:
        return self.repository.delete_by_id(workstep_id)

    def update_workstep(self, workstep_id: int, **kwargs) -> Optional[WorkStep]:
        return self.repository.update_workstep(workstep_id, **kwargs)
