# services/configuration_service.py

from typing import List, Optional, Dict, Any
from datetime import datetime
from webapp.ADM.maintenance.configuration.models.configuration_model import MaintenanceConfiguration
from webapp.ADM.maintenance.configuration.repositories.configuration_repository import ConfigurationRepository

class ConfigurationService:
    def __init__(self, configuration_repository: ConfigurationRepository):
        self.configuration_repository = configuration_repository

    def get_all_configurations(self) -> List[Dict[str, Any]]:
        configurations = self.configuration_repository.get_all_configurations()
        return [self._to_dict(config) for config in configurations]

    def get_configuration_by_id(self, config_id: int) -> Optional[Dict[str, Any]]:
        configuration = self.configuration_repository.get_configuration_by_id(config_id)
        return self._to_dict(configuration) if configuration else None

    def add_configuration(self, **kwargs) -> Dict[str, Any]:
        # Set action_date to current time if not provided
        if 'action_date' not in kwargs:
            kwargs['action_date'] = datetime.utcnow()
            
        configuration = MaintenanceConfiguration(**kwargs)
        created_configuration = self.configuration_repository.create_configuration(configuration)
        return self._to_dict(created_configuration)

    def update_configuration(self, config_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        # Update action_date if state is being changed
        if 'state' in kwargs:
            kwargs['action_date'] = datetime.utcnow()
            
        updated_configuration = self.configuration_repository.update_configuration(config_id, **kwargs)
        return self._to_dict(updated_configuration) if updated_configuration else None

    def delete_configuration(self, config_id: int) -> bool:
        return self.configuration_repository.delete_configuration(config_id)

    @staticmethod
    def _to_dict(configuration: MaintenanceConfiguration) -> Dict[str, Any]:
        return {
            "id": configuration.id,
            "name": configuration.name,
            "description": configuration.description,
            "url": configuration.url,
            "port": configuration.port,
            "refresh_time": configuration.refresh_time,
            "state": configuration.state,
            "action_date": configuration.action_date,
            "created_at": configuration.created_at,
            "updated_at": configuration.updated_at,
            "station_id": configuration.station_id
        }
