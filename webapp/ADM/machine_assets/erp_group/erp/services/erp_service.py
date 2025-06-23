# services/erp_group_service.py

from typing import List, Optional
from webapp.ADM.machine_assets.erp_group.erp.models.erp_model import ERPGroup
from webapp.ADM.machine_assets.erp_group.erp.repositories.erp_repositorie import ERPGroupRepository
from webapp.ADM.machine_assets.erp_group.erp.schemas.erp_schema import ERPGroupCreate, ERPGroupResponse

class ERPGroupService:
    def __init__(self, erp_group_repository: ERPGroupRepository) -> None:
        self.erp_group_repository = erp_group_repository

    def get_all_erp_groups(self) -> List[ERPGroupResponse]:
        """Get all ERP groups."""
        erp_groups = self.erp_group_repository.get_all()
        return [ERPGroupResponse(**erp_group) for erp_group in erp_groups]

    def get_erp_group_by_id(self, erp_group_id: int) -> Optional[ERPGroupResponse]:
        """Get an ERP group by ID."""
        erp_group = self.erp_group_repository.get_by_id(erp_group_id)
        if erp_group:
            return ERPGroupResponse(**erp_group)
        return None

    def add_erp_group(self, erp_group_data: ERPGroupCreate) -> ERPGroupResponse:
        """Add a new ERP group."""
        # Convert Pydantic model to SQLAlchemy model
        erp_group = ERPGroup(**erp_group_data.dict())
        # Add to repository
        erp_group_dict = self.erp_group_repository.add(erp_group)
        return ERPGroupResponse(**erp_group_dict)

    def delete_erp_group(self, erp_group_id: int) -> bool:
        """Delete an ERP group."""
        return self.erp_group_repository.delete_by_id(erp_group_id)

    def update_erp_group(self, erp_group_id: int, **kwargs) -> Optional[ERPGroupResponse]:
        """Update an ERP group."""
        erp_group = self.erp_group_repository.update(erp_group_id, **kwargs)
        if erp_group:
            return ERPGroupResponse(**erp_group)
        return None
