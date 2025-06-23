from typing import List

from webapp.ADM.master_data.workplan_data.workplan.models.workplan_model import WorkPlan
from webapp.ADM.master_data.workplan_data.workplan.repositories.workplan_repository import WorkPlanRepository


class WorkPlanService:
    def __init__(self, repository: WorkPlanRepository):
        self.repository = repository

    def get_all_work_plans(self) -> List[WorkPlan]:
        return self.repository.get_all()

    def get_work_plan_by_id(self, workplan_id: int) -> WorkPlan:
        return self.repository.get_by_id(workplan_id)

    def add_work_plan(self, **kwargs) -> WorkPlan:
        # Enforce field length constraints
        if 'workplan_status' in kwargs and kwargs['workplan_status']:
            # workplan_status is VARCHAR(1)
            kwargs['workplan_status'] = kwargs['workplan_status'][:1]
            
        if 'workplan_type' in kwargs and kwargs['workplan_type']:
            # workplan_type is VARCHAR(3)
            kwargs['workplan_type'] = kwargs['workplan_type'][:3]
            
        if 'part_no' in kwargs and kwargs['part_no']:
            # part_no is VARCHAR(80)
            kwargs['part_no'] = kwargs['part_no'][:80]
            
        if 'part_desc' in kwargs and kwargs['part_desc']:
            # part_desc is VARCHAR(80)
            kwargs['part_desc'] = kwargs['part_desc'][:80]
            
        if 'workplan_desc' in kwargs and kwargs['workplan_desc']:
            # workplan_desc is VARCHAR(80)
            kwargs['workplan_desc'] = kwargs['workplan_desc'][:80]
            
        if 'workplan_info' in kwargs and kwargs['workplan_info']:
            # workplan_info is VARCHAR(255)
            kwargs['workplan_info'] = kwargs['workplan_info'][:255]
            
        if 'workplan_version_erp' in kwargs and kwargs['workplan_version_erp']:
            # workplan_version_erp is VARCHAR(30)
            kwargs['workplan_version_erp'] = kwargs['workplan_version_erp'][:30]
            
        # Add the work plan with the validated data
        return self.repository.add(**kwargs)

    def delete_work_plan(self, workplan_id: int) -> bool:
        return self.repository.delete_by_id(workplan_id)

    def update_work_plan(self, workplan_id: int, **kwargs) -> WorkPlan:
        # Enforce field length constraints
        if 'workplan_status' in kwargs and kwargs['workplan_status']:
            # workplan_status is VARCHAR(1)
            kwargs['workplan_status'] = kwargs['workplan_status'][:1]
            
        if 'workplan_type' in kwargs and kwargs['workplan_type']:
            # workplan_type is VARCHAR(3)
            kwargs['workplan_type'] = kwargs['workplan_type'][:3]
            
        if 'part_no' in kwargs and kwargs['part_no']:
            # part_no is VARCHAR(80)
            kwargs['part_no'] = kwargs['part_no'][:80]
            
        if 'part_desc' in kwargs and kwargs['part_desc']:
            # part_desc is VARCHAR(80)
            kwargs['part_desc'] = kwargs['part_desc'][:80]
            
        if 'workplan_desc' in kwargs and kwargs['workplan_desc']:
            # workplan_desc is VARCHAR(80)
            kwargs['workplan_desc'] = kwargs['workplan_desc'][:80]
            
        if 'workplan_info' in kwargs and kwargs['workplan_info']:
            # workplan_info is VARCHAR(255)
            kwargs['workplan_info'] = kwargs['workplan_info'][:255]
            
        if 'workplan_version_erp' in kwargs and kwargs['workplan_version_erp']:
            # workplan_version_erp is VARCHAR(30)
            kwargs['workplan_version_erp'] = kwargs['workplan_version_erp'][:30]
            
        # Update the work plan with the validated data
        return self.repository.update_work_plan(workplan_id, **kwargs)
