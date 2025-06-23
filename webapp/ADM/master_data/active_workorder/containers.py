"""Active Workorder module container."""
from dependency_injector import containers, providers

from webapp.ADM.master_data.active_workorder.repositories.active_workorder_repository import ActiveWorkorderRepository
from webapp.ADM.master_data.active_workorder.services.active_workorder_service import ActiveWorkorderService


class ActiveWorkorderContainer(containers.DeclarativeContainer):
    """Active Workorder module container."""

    # Dependencies
    db = providers.Dependency()

    # Repositories
    active_workorder_repository = providers.Factory(
        ActiveWorkorderRepository,
        session_factory=db.provided.session
    )

    # Services
    active_workorder_service = providers.Factory(
        ActiveWorkorderService,
        active_workorder_repository=active_workorder_repository
    )
