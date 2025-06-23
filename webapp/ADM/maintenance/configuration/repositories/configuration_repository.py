# repositories/configuration_repository.py

from typing import List, Optional
from sqlalchemy.orm import Session
from contextlib import AbstractContextManager
from webapp.ADM.maintenance.configuration.models.configuration_model import MaintenanceConfiguration

class ConfigurationRepository:
    def __init__(self, session_factory: AbstractContextManager[Session]):
        self.session_factory = session_factory

    def get_all_configurations(self) -> List[MaintenanceConfiguration]:
        with self.session_factory() as session:
            return session.query(MaintenanceConfiguration).all()

    def get_configuration_by_id(self, config_id: int) -> Optional[MaintenanceConfiguration]:
        with self.session_factory() as session:
            return session.query(MaintenanceConfiguration).filter(MaintenanceConfiguration.id == config_id).first()

    def create_configuration(self, configuration: MaintenanceConfiguration) -> MaintenanceConfiguration:
        with self.session_factory() as session:
            session.add(configuration)
            session.commit()
            session.refresh(configuration)
            return configuration

    def update_configuration(self, config_id: int, **kwargs) -> Optional[MaintenanceConfiguration]:
        with self.session_factory() as session:
            configuration = session.query(MaintenanceConfiguration).filter(MaintenanceConfiguration.id == config_id).first()
            if configuration:
                for key, value in kwargs.items():
                    if value is not None:
                        setattr(configuration, key, value)
                session.commit()
                session.refresh(configuration)
            return configuration

    def delete_configuration(self, config_id: int) -> bool:
        with self.session_factory() as session:
            configuration = session.query(MaintenanceConfiguration).filter(MaintenanceConfiguration.id == config_id).first()
            if configuration:
                session.delete(configuration)
                session.commit()
                return True
            return False
