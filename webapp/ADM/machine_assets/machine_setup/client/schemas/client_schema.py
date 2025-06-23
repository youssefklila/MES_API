# schemas.py or within the endpoints module
from pydantic import BaseModel, ConfigDict

class ClientBase(BaseModel):
    user_id: int
    company_code: str
    name: str
    description: str

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)