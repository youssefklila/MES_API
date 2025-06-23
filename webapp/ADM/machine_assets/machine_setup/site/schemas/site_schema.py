# schemas/site_schema.py

from pydantic import BaseModel
from typing import Optional

class SiteBase(BaseModel):
    user_id: int
    site_number: str
    site_external_number: Optional[str] = None
    deletion_priority: Optional[int] = None
    geo_coordinates: Optional[str] = None
    description: Optional[str] = None
    company_code_id: Optional[int] = None

class SiteCreate(SiteBase):
    pass

class SiteUpdate(BaseModel):
    user_id: Optional[int] = None
    site_number: Optional[str] = None
    site_external_number: Optional[str] = None
    deletion_priority: Optional[int] = None
    geo_coordinates: Optional[str] = None
    description: Optional[str] = None
    company_code_id: Optional[int] = None

class SiteResponse(SiteBase):
    id: int

    class Config:
        orm_mode = True
