# schemas/assign_stations_to_erpgrp_schema.py

from typing import Optional

from pydantic import BaseModel


class AssignStationsToErpGrpBase(BaseModel):
    station_id: int
    erp_group_id: int
    station_type: Optional[str] = None
    user_id: int

class AssignStationsToErpGrpCreate(AssignStationsToErpGrpBase):
    pass

class AssignStationsToErpGrpResponse(AssignStationsToErpGrpBase):
    id: int

    class Config:
        orm_mode = True
