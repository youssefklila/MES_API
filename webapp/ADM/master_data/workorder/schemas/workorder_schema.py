from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


# Base schema for WorkOrder
class WorkOrderBase(BaseModel):
    # Required fields
    workorder_no: str = Field(..., max_length=80)
    workorder_type: str = Field(..., max_length=120)
    part_number: str = Field(..., max_length=80)
    workorder_qty: float = Field(...)
    startdate: datetime
    deliverydate: datetime
    unit: str = Field(..., max_length=5)
    bom_version: str = Field(..., max_length=30)
    workplan_type: str = Field(..., max_length=3)
    backflush: str = Field(..., max_length=1)
    source: float
    
    # Optional fields
    workorder_desc: Optional[str] = Field(None, max_length=80)
    bom_info: Optional[str] = Field(None, max_length=20)
    workplan_valid_from: Optional[datetime] = None
    workorder_no_ext: Optional[str] = Field(None, max_length=40)
    info1: Optional[str] = Field(None, max_length=512)
    info2: Optional[str] = Field(None, max_length=512)
    info3: Optional[str] = Field(None, max_length=512)
    info4: Optional[str] = Field(None, max_length=512)
    status: Optional[float] = None
    created: Optional[datetime] = None
    stamp: Optional[datetime] = None
    site_id: Optional[int] = None
    client_id: Optional[int] = None
    company_id: Optional[int] = None
    drawing_no: Optional[str] = Field(None, max_length=40)
    workorder_state: Optional[str] = Field(None, max_length=1)
    parent_workorder: Optional[str] = Field(None, max_length=30)
    controller: Optional[str] = Field(None, max_length=20)
    info5: Optional[str] = Field(None, max_length=512)
    ninfo1: Optional[float] = None
    ninfo2: Optional[float] = None
    bareboard_no: Optional[str] = Field(None, max_length=80)
    workplan_vers: Optional[int] = None
    aps_planning_start_date: Optional[datetime] = None
    aps_planning_stamp: Optional[datetime] = None
    aps_planning_end_date: Optional[datetime] = None
    aps_order_fixation: Optional[float] = None


# Schema for creating a WorkOrder
class WorkOrderCreate(WorkOrderBase):
    pass


# Schema for updating a WorkOrder
class WorkOrderUpdate(BaseModel):
    # All fields are optional for updates
    workorder_no: Optional[str] = Field(None, max_length=80)
    workorder_type: Optional[str] = Field(None, max_length=5)
    part_number: Optional[str] = Field(None, max_length=80)
    workorder_qty: Optional[float] = None
    startdate: Optional[datetime] = None
    deliverydate: Optional[datetime] = None
    unit: Optional[str] = Field(None, max_length=5)
    bom_version: Optional[str] = Field(None, max_length=30)
    workplan_type: Optional[str] = Field(None, max_length=3)
    backflush: Optional[str] = Field(None, max_length=1)
    source: Optional[float] = None
    workorder_desc: Optional[str] = Field(None, max_length=80)
    bom_info: Optional[str] = Field(None, max_length=20)
    workplan_valid_from: Optional[datetime] = None
    workorder_no_ext: Optional[str] = Field(None, max_length=40)
    info1: Optional[str] = Field(None, max_length=512)
    info2: Optional[str] = Field(None, max_length=512)
    info3: Optional[str] = Field(None, max_length=512)
    info4: Optional[str] = Field(None, max_length=512)
    status: Optional[float] = None
    created: Optional[datetime] = None
    stamp: Optional[datetime] = None
    site_id: Optional[int] = None
    client_id: Optional[int] = None
    company_id: Optional[int] = None
    drawing_no: Optional[str] = Field(None, max_length=40)
    workorder_state: Optional[str] = Field(None, max_length=1)
    parent_workorder: Optional[str] = Field(None, max_length=30)
    controller: Optional[str] = Field(None, max_length=20)
    info5: Optional[str] = Field(None, max_length=512)
    ninfo1: Optional[float] = None
    ninfo2: Optional[float] = None
    bareboard_no: Optional[str] = Field(None, max_length=80)
    workplan_vers: Optional[int] = None
    aps_planning_start_date: Optional[datetime] = None
    aps_planning_stamp: Optional[datetime] = None
    aps_planning_end_date: Optional[datetime] = None
    aps_order_fixation: Optional[float] = None


# Schema for WorkOrder response
class WorkOrderResponse(WorkOrderBase):
    id: int

    class Config:
        from_attributes = True


# Schema for paginated WorkOrder response
class PaginatedWorkOrders(BaseModel):
    items: List[WorkOrderResponse]
    total: int
    page: int
    size: int
    pages: int