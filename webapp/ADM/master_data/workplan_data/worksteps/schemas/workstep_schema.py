from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


# Base schema for WorkStep
class WorkStepBase(BaseModel):
    workplan_id: int
    erp_group_id: Optional[int] = None
    workstep_desc: Optional[str] = None
    erp_grp_no: Optional[str] = None
    erp_grp_desc: Optional[str] = None
    step: Optional[float] = None
    confirmation: Optional[str] = None
    sequentiell: Optional[str] = None
    workstep_type: Optional[str] = None
    setup_time: Optional[float] = None
    te_person: Optional[float] = None
    te_machine: Optional[float] = None
    te_time_base: Optional[float] = None
    time_unit: Optional[str] = None
    te_qty_base: Optional[float] = None
    transport_time: Optional[float] = None
    wait_time: Optional[float] = None
    status: Optional[float] = None
    stamp: Optional[datetime] = None
    traceflag: Optional[str] = None
    setup_flag: Optional[str] = None
    equ_id: Optional[float] = None
    workstep_version_erp: Optional[str] = None
    msl_relevant: Optional[float] = None
    msl_offset: Optional[float] = None
    info: Optional[str] = None


# Schema for creating a WorkStep
class WorkStepCreate(WorkStepBase):
    pass


# Schema for updating a WorkStep
class WorkStepUpdate(BaseModel):
    workplan_id: Optional[int] = None
    erp_group_id: Optional[int] = None
    workstep_desc: Optional[str] = None
    erp_grp_no: Optional[str] = None
    erp_grp_desc: Optional[str] = None
    step: Optional[float] = None
    confirmation: Optional[str] = None
    sequentiell: Optional[str] = None
    workstep_type: Optional[str] = None
    setup_time: Optional[float] = None
    te_person: Optional[float] = None
    te_machine: Optional[float] = None
    te_time_base: Optional[float] = None
    time_unit: Optional[str] = None
    te_qty_base: Optional[float] = None
    transport_time: Optional[float] = None
    wait_time: Optional[float] = None
    status: Optional[float] = None
    stamp: Optional[datetime] = None
    traceflag: Optional[str] = None
    setup_flag: Optional[str] = None
    equ_id: Optional[float] = None
    workstep_version_erp: Optional[str] = None
    msl_relevant: Optional[float] = None
    msl_offset: Optional[float] = None
    info: Optional[str] = None


# Schema for WorkStep response
class WorkStep(WorkStepBase):
    id: int

    class Config:
        orm_mode = True


# Schema for paginated WorkStep response
class PaginatedWorkSteps(BaseModel):
    items: List[WorkStep]
    total: int
    page: int
    size: int
    pages: int
