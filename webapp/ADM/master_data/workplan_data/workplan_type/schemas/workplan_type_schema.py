from pydantic import BaseModel
from typing import Optional

class WorkPlanTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

class WorkPlanTypeCreate(WorkPlanTypeBase):
    pass

class WorkPlanTypeUpdate(WorkPlanTypeBase):
    pass

class WorkPlanTypeResponse(WorkPlanTypeBase):
    id: int
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
