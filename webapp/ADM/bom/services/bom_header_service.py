from typing import List, Optional, Dict
from datetime import datetime
from webapp.ADM.bom.repositories.bom_header_repository import BomHeaderRepository
from webapp.ADM.bom.schemas.bom_header_schema import BomHeaderCreate, BomHeaderUpdate, BomHeaderResponse

class BomHeaderService:
    def __init__(self, bom_header_repository: BomHeaderRepository):
        self.bom_header_repository = bom_header_repository

    def get_all_bom_headers(self) -> List[BomHeaderResponse]:
        bom_headers = self.bom_header_repository.get_all()
        return [BomHeaderResponse(**bom_header) for bom_header in bom_headers]

    def get_bom_header_by_id(self, bom_header_id: int) -> Optional[BomHeaderResponse]:
        bom_header = self.bom_header_repository.get_by_id(bom_header_id)
        return BomHeaderResponse(**bom_header) if bom_header else None

    def create_bom_header(self, bom_header: BomHeaderCreate) -> BomHeaderResponse:
        # Add last_updated timestamp
        bom_header_dict = bom_header.dict()
        bom_header_dict['last_updated'] = datetime.now()
        
        created_bom_header = self.bom_header_repository.create(**bom_header_dict)
        return BomHeaderResponse(**created_bom_header)

    def update_bom_header(self, bom_header_id: int, bom_header: BomHeaderUpdate) -> Optional[BomHeaderResponse]:
        # Add last_updated timestamp
        bom_header_dict = bom_header.dict(exclude_unset=True)
        bom_header_dict['last_updated'] = datetime.now()
        
        updated_bom_header = self.bom_header_repository.update(bom_header_id, **bom_header_dict)
        return BomHeaderResponse(**updated_bom_header) if updated_bom_header else None

    def delete_bom_header(self, bom_header_id: int) -> bool:
        return self.bom_header_repository.delete(bom_header_id)