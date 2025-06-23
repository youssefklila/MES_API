from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


# Base schema for WorkPlan
class WorkPlanBase(BaseModel):
    user_id: int
    site_id: Optional[int] = None
    client_id: Optional[int] = None
    company_id: Optional[int] = None
    source: Optional[float] = None
    status: Optional[float] = None
    product_vers_id: Optional[float] = None
    workplan_status: Optional[str] = None
    part_no: Optional[str] = None
    part_desc: Optional[str] = None
    workplan_desc: Optional[str] = None
    workplan_type: Optional[str] = None
    workplan_info: Optional[str] = None
    workplan_version_erp: Optional[str] = None
    aps_info1: Optional[str] = None
    aps_info2: Optional[str] = None
    created: Optional[datetime] = None
    stamp: Optional[datetime] = None
    workplan_valid_from: Optional[datetime] = None
    workplan_valid_to: Optional[datetime] = None


# Schema for creating a WorkPlan
class WorkPlanCreate(WorkPlanBase):
    pass


# Schema for updating a WorkPlan
class WorkPlanUpdate(BaseModel):
    user_id: Optional[int] = None
    site_id: Optional[int] = None
    client_id: Optional[int] = None
    company_id: Optional[int] = None
    source: Optional[float] = None
    status: Optional[float] = None
    product_vers_id: Optional[float] = None
    workplan_status: Optional[str] = None
    part_no: Optional[str] = None
    part_desc: Optional[str] = None
    workplan_desc: Optional[str] = None
    workplan_type: Optional[str] = None
    workplan_info: Optional[str] = None
    workplan_version_erp: Optional[str] = None
    aps_info1: Optional[str] = None
    aps_info2: Optional[str] = None
    created: Optional[datetime] = None
    stamp: Optional[datetime] = None
    workplan_valid_from: Optional[datetime] = None
    workplan_valid_to: Optional[datetime] = None


# Schema for WorkPlan response
class WorkPlan(WorkPlanBase):
    id: int

    class Config:
        orm_mode = True


# Schema for paginated WorkPlan response
class PaginatedWorkPlans(BaseModel):
    items: List[WorkPlan]
    total: int
    page: int
    size: int
    pages: int
