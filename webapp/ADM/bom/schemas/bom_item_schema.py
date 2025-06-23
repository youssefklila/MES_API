from pydantic import BaseModel, Field, validator
from typing import Optional, List

class BomItemBase(BaseModel):
    bom_header_id: int
    part_master_id: int
    quantity: int = Field(gt=0)
    is_product: bool = False
    component_name: str

class BomItemCreate(BomItemBase):
    pass

class BomItemUpdate(BaseModel):
    part_master_id: Optional[int] = None
    quantity: Optional[int] = Field(None, gt=0)
    is_product: Optional[bool] = None
    component_name: Optional[str] = None

class BomItemResponse(BomItemBase):
    id: int
    component_names: List[str] = []
    
    @validator('component_names', always=True)
    def generate_component_names(cls, v, values):
        # Always return a list, even if empty
        if not v:
            v = []
            
        if 'component_name' in values and 'quantity' in values:
            quantity = values['quantity']
            component_name = values['component_name']
            return [component_name] * quantity
        return v
    
    class Config:
        from_attributes = True
        orm_mode = True