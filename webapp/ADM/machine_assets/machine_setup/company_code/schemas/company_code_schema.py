# schemas/company_code_schema.py

from pydantic import BaseModel, ConfigDict
from typing import Optional

class CompanyCodeBase(BaseModel):
    user_id: int
    client_id: int
    name: str
    description: str

class CompanyCodeCreate(CompanyCodeBase):
    pass

class CompanyCodeUpdate(CompanyCodeBase):
    pass

class CompanyCodeOut(CompanyCodeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
