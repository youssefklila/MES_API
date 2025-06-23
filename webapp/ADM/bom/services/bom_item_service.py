from typing import List, Optional, Dict
from webapp.ADM.bom.repositories.bom_item_repository import BomItemRepository
from webapp.ADM.bom.schemas.bom_item_schema import BomItemCreate, BomItemUpdate, BomItemResponse

class BomItemService:
    def __init__(self, bom_item_repository: BomItemRepository):
        self.bom_item_repository = bom_item_repository

    def get_all_bom_items(self) -> List[BomItemResponse]:
        bom_items = self.bom_item_repository.get_all()
        return [BomItemResponse(**bom_item) for bom_item in bom_items]

    def get_bom_item_by_id(self, bom_item_id: int) -> Optional[BomItemResponse]:
        bom_item = self.bom_item_repository.get_by_id(bom_item_id)
        return BomItemResponse(**bom_item) if bom_item else None

    def get_bom_items_by_header_id(self, bom_header_id: int) -> List[BomItemResponse]:
        bom_items = self.bom_item_repository.get_by_bom_header_id(bom_header_id)
        return [BomItemResponse(**bom_item) for bom_item in bom_items]

    def create_bom_item(self, bom_item: BomItemCreate) -> BomItemResponse:
        created_bom_item = self.bom_item_repository.create(**bom_item.dict())
        return BomItemResponse(**created_bom_item)

    def update_bom_item(self, bom_item_id: int, bom_item: BomItemUpdate) -> Optional[BomItemResponse]:
        updated_bom_item = self.bom_item_repository.update(bom_item_id, **bom_item.dict(exclude_unset=True))
        return BomItemResponse(**updated_bom_item) if updated_bom_item else None

    def delete_bom_item(self, bom_item_id: int) -> bool:
        return self.bom_item_repository.delete(bom_item_id) 