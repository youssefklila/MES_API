"""Containers module."""

from dependency_injector import containers, providers
from fastapi.security import OAuth2PasswordBearer
from IIOT.ADM.machine_assets.machine_setup.user.repositories.user_repositorie import UserRepository
from IIOT.ADM.machine_assets.machine_setup.user.services.user_service import UserService
from IIOT.monitoring.tasks.repositories.task_repository import TaskRepository
from IIOT.monitoring.tasks.services.task_service import TaskService
from IIOT.monitoring.reports.repositories.report_repository import ReportRepository
from IIOT.monitoring.reports.services.report_service import ReportService
from IIOT.database import Database
from IIOT.auth.auth_service import AuthService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "IIOT.ADM.machine_assets.machine_setup.user.endpoints.user_endpoint",
            "IIOT.auth.endpoints",
            "IIOT.auth.dependencies",
            "IIOT.iot.endpoints",
            "IIOT.iot.dependencies",
            "IIOT.monitoring.tasks.endpoints.task_endpoint",
            "IIOT.monitoring.reports.endpoints.report_endpoint",
        ]
    )

    # Config and Core Services
    config = providers.Configuration(yaml_files=["iiot_config.yml"])
    oauth2_scheme = providers.Object(OAuth2PasswordBearer(tokenUrl="/auth/token"))

    # Database
    db = providers.Singleton(Database, db_url=config.db.url)

    # User Services
    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    # Auth Service
    auth_service = providers.Factory(
        AuthService,
        db=db,
        user_service=user_service,
    )

    # Monitoring Services
    task_repository = providers.Factory(
        TaskRepository,
        session_factory=db.provided.session,
    )

    task_service = providers.Factory(
        TaskService,
        task_repository=task_repository,
    )

    report_repository = providers.Factory(
        ReportRepository,
        session_factory=db.provided.session,
    )

    report_service = providers.Factory(
        ReportService,
        report_repository=report_repository,
    )

    # IoT Services
    mqtt_client = providers.Singleton(
        "IIOT.iot.mqtt_client.MQTTClient",
        host=config.mqtt.host.as_(str) if config.mqtt.host() else "localhost",
        port=config.mqtt.port.as_(int) if config.mqtt.port() else 1883,
        keepalive=config.mqtt.keepalive.as_(int) if config.mqtt.keepalive() else 60,
    )
    
    iot_service = providers.Factory(
        "IIOT.iot.service.IoTService",
        mqtt_client=mqtt_client
    )
    
    def init_resources(self):
        """Initialize resources like database tables."""
        db = self.db()
        db.create_database()