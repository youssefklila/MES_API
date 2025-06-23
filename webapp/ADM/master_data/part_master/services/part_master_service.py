from webapp.ADM.master_data.part_master.repositories.part_master_repository import PartMasterRepository
from webapp.ADM.master_data.part_master.schemas.part_master_schema import PartMasterResponse
from fastapi import HTTPException


class PartMasterService:
    def __init__(self, part_master_repository: PartMasterRepository):
        self.part_master_repository = part_master_repository

    def get_all_part_masters(self):
        part_masters = self.part_master_repository.get_all()
        return [PartMasterResponse.parse_obj(part_master) for part_master in part_masters]

    def get_part_master_by_id(self, part_master_id: int):
        part_master = self.part_master_repository.get_by_id(part_master_id)
        if part_master:
            return PartMasterResponse.parse_obj(part_master)
        return None

    def create_part_master(self, **kwargs):
        # Check if part number already exists
        existing_part = self.part_master_repository.get_by_part_number(kwargs.get('part_number'))
        if existing_part:
            raise HTTPException(
                status_code=400,
                detail=f"Part master with part number '{kwargs.get('part_number')}' already exists"
            )
        
        part_master = self.part_master_repository.create(**kwargs)
        return PartMasterResponse.parse_obj(part_master)

    def update_part_master(self, part_master_id: int, **kwargs):
        part_master = self.part_master_repository.update(part_master_id, **kwargs)
        if part_master:
            return PartMasterResponse.parse_obj(part_master)
        return None

    def delete_part_master(self, part_master_id: int) -> bool:
        return self.part_master_repository.delete(part_master_id)
