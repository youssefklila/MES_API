"""Containers module."""

from dependency_injector import containers, providers
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from webapp.ADM.machine_assets.erp_group.erp.repositories.erp_repositorie import ERPGroupRepository
from webapp.ADM.machine_assets.erp_group.erp.services.erp_service import ERPGroupService
from webapp.ADM.machine_assets.machine_setup.cell.repositories.cell_repositorie import CellRepository
from webapp.ADM.machine_assets.machine_setup.cell.services.cell_service import CellService
from webapp.ADM.machine_assets.machine_setup.client.repositories.client_repositorie import ClientRepository
from webapp.ADM.machine_assets.machine_setup.company_code.repositories.company_code_repositorie import CompanyCodeRepository
from webapp.ADM.machine_assets.machine_setup.company_code.services.company_code_service import CompanyCodeService
from webapp.ADM.machine_assets.machine_setup.machine_group.repositories.machine_group_repositorie import MachineGroupRepository
from webapp.ADM.machine_assets.machine_setup.machine_group.services.machine_group_service import MachineGroupService
from webapp.ADM.machine_assets.machine_setup.site.repositories.site_repositorie import SiteRepository
from webapp.ADM.machine_assets.machine_setup.site.services.site_service import SiteService
from webapp.ADM.machine_assets.machine_setup.station.repositories.station_repositorie import StationRepository
from webapp.ADM.machine_assets.machine_setup.station.services.station_service import StationService
from webapp.ADM.machine_assets.machine_setup.line.repositories.line_repository import LineRepository
from webapp.ADM.machine_assets.machine_setup.line.services.line_service import LineService
from webapp.ADM.machine_assets.machine_setup.user.repositories.user_repositorie import UserRepository
from webapp.ADM.machine_assets.machine_setup.user.services.user_service import UserService
from webapp.ADM.machine_assets.erp_group.assign_station.repositories.assign_stations_to_erpgrp_repository import AssignStationsToErpGrpRepository
from webapp.ADM.machine_assets.erp_group.assign_station.services.assign_stations_to_erpgrp_service import AssignStationsToErpGrpService
from webapp.ADM.machine_assets.machine_setup.client.services.client_service import ClientService
from webapp.ADM.master_data.part_group.group.repositories.part_group_repository import PartGroupRepository
from webapp.ADM.master_data.part_group.group.services.part_group_service import PartGroupService
from webapp.ADM.master_data.part_group.type.repositories.part_group_type_repository import PartGroupTypeRepository
from webapp.ADM.master_data.part_group.type.services.part_group_type_service import PartGroupTypeService
from webapp.ADM.master_data.part_master.repositories.part_master_repository import PartMasterRepository
from webapp.ADM.master_data.part_master.services.part_master_service import PartMasterService
from webapp.ADM.master_data.part_type.repositories.part_type_repository import PartTypeRepository
from webapp.ADM.master_data.part_type.services.part_type_service import PartTypeService
from webapp.ADM.master_data.unit.repositories.unit_repository import UnitRepository
from webapp.ADM.master_data.unit.services.unit_service import UnitService
from webapp.ADM.master_data.workplan_data.workplan.repositories.workplan_repository import WorkPlanRepository
from webapp.ADM.master_data.workplan_data.workplan.services.workplan_service import WorkPlanService
from webapp.ADM.master_data.workplan_data.workplan_type.repositories.workplan_type_repository import WorkPlanTypeRepository
from webapp.ADM.master_data.workplan_data.workplan_type.services.workplan_type_service import WorkPlanTypeService
from webapp.ADM.master_data.workplan_data.worksteps.repositories.workstep_repository import WorkStepRepository
from webapp.ADM.master_data.workplan_data.worksteps.services.workstep_service import WorkStepService
from webapp.ADM.master_data.workorder.repositories.workorder_repository import WorkOrderRepository
from webapp.ADM.master_data.workorder.services.workorder_service import WorkOrderService
from webapp.ADM.TRACKING.booking.repositories.booking_repository import BookingRepository
from webapp.ADM.TRACKING.booking.services.booking_service import BookingService
from webapp.ADM.TRACKING.failure_type.repositories.failure_type_repository import FailureTypeRepository
from webapp.ADM.TRACKING.failure_type.services.failure_type_service import FailureTypeService
from webapp.ADM.TRACKING.failure_group_type.repositories.failure_group_type_repository import FailureGroupTypeRepository
from webapp.ADM.TRACKING.failure_group_type.services.failure_group_type_service import FailureGroupTypeService
from webapp.ADM.TRACKING.measurement_data.repositories.measurement_data_repository import MeasurementDataRepository
from webapp.ADM.TRACKING.measurement_data.services.measurement_data_service import MeasurementDataService

# IIOT module
from webapp.IIOT.repositories.iiot_repository import IIOTSensorDataRepository
from webapp.IIOT.services.iiot_service import IIOTSensorDataService
from webapp.ADM.MDC.machine_condition_group.repositories.machine_condition_group_repository import MachineConditionGroupRepository
from webapp.ADM.MDC.machine_condition_group.services.machine_condition_group_service import MachineConditionGroupService
from webapp.ADM.MDC.machine_condition.repositories.machine_condition_repository import MachineConditionRepository
from webapp.ADM.MDC.machine_condition.services.machine_condition_service import MachineConditionService
from webapp.ADM.MDC.machine_condition_data.repositories.machine_condition_data_repository import MachineConditionDataRepository
from webapp.ADM.MDC.machine_condition_data.services.machine_condition_data_service import MachineConditionDataService
from webapp.database import Database
from webapp.auth.auth_service import AuthService
from webapp.ADM.bom.repositories.bom_repository import BomRepository
from webapp.ADM.bom.services.bom_service import BomService
from webapp.ADM.bom.repositories.bom_header_repository import BomHeaderRepository
from webapp.ADM.bom.services.bom_header_service import BomHeaderService
from webapp.ADM.bom.repositories.bom_item_repository import BomItemRepository
from webapp.ADM.bom.services.bom_item_service import BomItemService
from webapp.ADM.master_data.active_workorder.repositories.active_workorder_repository import ActiveWorkorderRepository
from webapp.ADM.master_data.active_workorder.services.active_workorder_service import ActiveWorkorderService
from webapp.ADM.maintenance.configuration.repositories.configuration_repository import ConfigurationRepository
from webapp.ADM.maintenance.configuration.services.configuration_service import ConfigurationService
from webapp.ADM.maintenance.localStorage.repositories.local_storage_repository import LocalStorageRepository
from webapp.ADM.maintenance.localStorage.services.local_storage_service import LocalStorageService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "webapp.ADM.machine_assets.machine_setup.user.endpoints.user_endpoint",
            "webapp.ADM.maintenance.localStorage.endpoints.local_storage_endpoint",
            "webapp.ADM.machine_assets.machine_setup.station.endpoints.station_endpoint",
            "webapp.ADM.machine_assets.machine_setup.cell.endpoints.cell_endpoint",
            "webapp.ADM.machine_assets.machine_setup.client.endpoints.client_endpoint",
            "webapp.ADM.machine_assets.machine_setup.company_code.endpoints.company_code_endpoint",
            "webapp.ADM.machine_assets.machine_setup.machine_group.endpoints.machine_group_endpoint",
            "webapp.ADM.machine_assets.machine_setup.site.endpoints.site_endpoint",
            "webapp.ADM.machine_assets.erp_group.erp.endpoints.erp_endpoint",
            "webapp.ADM.machine_assets.erp_group.assign_station.endpoints.assign_stations_to_erpgrp_endpoint",
            "webapp.ADM.master_data.part_type.endpoints.part_type_endpoint",
            "webapp.ADM.master_data.part_group.type.endpoints.part_group_type_endpoint",
            "webapp.ADM.master_data.part_group.group.endpoints.part_group_endpoint",
            "webapp.ADM.master_data.unit.endpoints.unit_endpoint",
            "webapp.ADM.master_data.part_master.endpoints.part_master_endpoint",
            "webapp.ADM.master_data.workplan_data.workplan_type.endpoints.workplan_type_endpoint",
            "webapp.ADM.master_data.workplan_data.workplan.endpoints.workplan_endpoint",
            "webapp.ADM.master_data.workplan_data.worksteps.endpoints.workstep_endpoint",
            "webapp.ADM.master_data.workorder.endpoints.workorder_endpoint",
            "webapp.ADM.TRACKING.booking.endpoints.booking_endpoint",
            "webapp.ADM.TRACKING.failure_type.endpoints.failure_type_endpoint",
            "webapp.ADM.TRACKING.failure_group_type.endpoints.failure_group_type_endpoint",
            "webapp.ADM.TRACKING.measurement_data.endpoints.measurement_data_endpoint",
            "webapp.ADM.MDC.machine_condition_group.endpoints.machine_condition_group_endpoint",
            "webapp.ADM.MDC.machine_condition.endpoints.machine_condition_endpoint",
            "webapp.ADM.MDC.machine_condition_data.endpoints.machine_condition_data_endpoint",
            "webapp.ADM.bom.endpoints.bom_header_endpoint",
            "webapp.ADM.bom.endpoints.bom_item_endpoint",
            "webapp.ADM.master_data.active_workorder.endpoints.active_workorder_endpoint",
            "webapp.auth.endpoints",
            "webapp.auth.dependencies",
            "webapp.ADM.machine_assets.machine_setup.client.endpoints.client_endpoint",
            "webapp.ADM.machine_assets.machine_setup.user.endpoints.user_endpoint",
        ],
        packages=["webapp"],
    )
    
    oauth2_scheme = providers.Object(OAuth2PasswordBearer(tokenUrl="auth/token"))
    config = providers.Configuration(yaml_files=["config.yml"])
    db = providers.Singleton(Database, db_url=config.db.url)
    
    client_repository = providers.Factory(
        ClientRepository,
        session_factory=db.provided.session,
    )
    client_service = providers.Factory(
        ClientService,
        client_repository=client_repository,
    )
    
    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
    
    auth_service = providers.Factory(
        AuthService,
        db=db,
        user_service=user_service,
    )
    
    company_code_repository = providers.Factory(
        CompanyCodeRepository,
        session_factory=db.provided.session,
    )
    company_code_service = providers.Factory(
        CompanyCodeService,
        company_code_repository=company_code_repository,
    )
    
    cell_repository = providers.Factory(
        CellRepository,
        session_factory=db.provided.session,
    )
    cell_service = providers.Factory(
        CellService,
        cell_repository=cell_repository,
    )
    
    site_repository = providers.Factory(
        SiteRepository,
        session_factory=db.provided.session,
    )
    site_service = providers.Factory(
        SiteService,
        site_repository=site_repository,
    )
    
    machine_group_repository = providers.Factory(
        MachineGroupRepository,
        session_factory=db.provided.session,
    )
    machine_group_service = providers.Factory(
        MachineGroupService,
        machine_group_repository=machine_group_repository,
    )
    
    station_repository = providers.Factory(
        StationRepository,
        session_factory=db.provided.session,
    )
    station_service = providers.Factory(
        StationService,
        station_repository=station_repository,
    )
    
    erp_group_repository = providers.Factory(
        ERPGroupRepository,
        session_factory=db.provided.session,
    )
    erp_group_service = providers.Factory(
        ERPGroupService,
        erp_group_repository=erp_group_repository,
    )
    
    assign_stations_to_erpgrp_repository = providers.Factory(
        AssignStationsToErpGrpRepository,
        session_factory=db.provided.session,
    )
    assign_stations_to_erpgrp_service = providers.Factory(
        AssignStationsToErpGrpService,
        assign_stations_to_erpgrp_repository=assign_stations_to_erpgrp_repository,
    )
    
    part_type_repository = providers.Factory(
        PartTypeRepository,
        session_factory=db.provided.session,
    )
    part_type_service = providers.Factory(
        PartTypeService,
        repository=part_type_repository,
    )
    
    part_group_type_repository = providers.Factory(
        PartGroupTypeRepository,
        session_factory=db.provided.session,
    )
    part_group_type_service = providers.Factory(
        PartGroupTypeService,
        repository=part_group_type_repository,
    )
    
    part_group_repository = providers.Factory(
        PartGroupRepository,
        session_factory=db.provided.session)
    part_group_service = providers.Factory(
        PartGroupService,
        repository=part_group_repository)
    
    unit_repository = providers.Factory(
        UnitRepository,
        session_factory=db.provided.session,
    )
    unit_service = providers.Factory(
        UnitService,
        repository=unit_repository,
    )
    
    part_master_repository = providers.Factory(
        PartMasterRepository,
        session_factory=db.provided.session,
    )
    part_master_service = providers.Factory(
        PartMasterService,
        part_master_repository=part_master_repository,
    )
    
    workplan_type_repository = providers.Factory(
        WorkPlanTypeRepository,
        session_factory=db.provided.session,
    )
    workplan_type_service = providers.Factory(
        WorkPlanTypeService,
        workplan_type_repository=workplan_type_repository,
    )
    
    work_plan_repository = providers.Factory(
        WorkPlanRepository,
        session_factory=db.provided.session,
    )
    work_plan_service = providers.Factory(
        WorkPlanService,
        repository=work_plan_repository,
    )
    
    workstep_repository = providers.Factory(
        WorkStepRepository,
        session_factory=db.provided.session,
    )
    workstep_service = providers.Factory(
        WorkStepService,
        repository=workstep_repository,
    )
    
    workorder_repository = providers.Factory(
        WorkOrderRepository,
        session_factory=db.provided.session,
    )
    workorder_service = providers.Factory(
        WorkOrderService,
        repository=workorder_repository,
    )
    
    booking_repository = providers.Factory(
        BookingRepository,
        session_factory=db.provided.session,
    )
    booking_service = providers.Factory(
        BookingService,
        repository=booking_repository,
    )
    
    failure_type_repository = providers.Factory(
        FailureTypeRepository,
        session_factory=db.provided.session,
    )
    failure_type_service = providers.Factory(
        FailureTypeService,
        failure_type_repository=failure_type_repository,
    )
    
    failure_group_type_repository = providers.Factory(
        FailureGroupTypeRepository,
        session_factory=db.provided.session,
    )
    failure_group_type_service = providers.Factory(
        FailureGroupTypeService,
        failure_group_type_repository=failure_group_type_repository,
    )
    
    measurement_data_repository = providers.Factory(
        MeasurementDataRepository,
        session_factory=db.provided.session,
    )
    measurement_data_service = providers.Factory(
        MeasurementDataService,
        measurement_data_repository=measurement_data_repository,
    )
    
    # IIOT Services
    iiot_sensor_data_repository = providers.Factory(
        IIOTSensorDataRepository,
        session_factory=db.provided.session,
    )
    iiot_sensor_data_service = providers.Factory(
        IIOTSensorDataService,
        iiot_repository=iiot_sensor_data_repository,
    )
    
    bom_repository = providers.Factory(
        BomRepository,
        session_factory=db.provided.session
    )
    bom_service = providers.Factory(
        BomService,
        bom_repository=bom_repository
    )
    
    bom_header_repository = providers.Factory(
        BomHeaderRepository,
        session_factory=db.provided.session
    )
    bom_header_service = providers.Factory(
        BomHeaderService,
        bom_header_repository=bom_header_repository
    )
    
    bom_item_repository = providers.Factory(
        BomItemRepository,
        session_factory=db.provided.session
    )
    bom_item_service = providers.Factory(
        BomItemService,
        bom_item_repository=bom_item_repository
    )
    
    # Active Workorder Services
    active_workorder_repository = providers.Factory(
        ActiveWorkorderRepository,
        session_factory=db.provided.session
    )
    active_workorder_service = providers.Factory(
        ActiveWorkorderService,
        active_workorder_repository=active_workorder_repository
    )
    
    machine_condition_group_repository = providers.Factory(
        MachineConditionGroupRepository,
        session_factory=db.provided.session
    )
    machine_condition_group_service = providers.Factory(
        MachineConditionGroupService,
        repository=machine_condition_group_repository
    )
    
    machine_condition_repository = providers.Factory(
        MachineConditionRepository,
        session_factory=db.provided.session
    )
    machine_condition_service = providers.Factory(
        MachineConditionService,
        repository=machine_condition_repository
    )
    
    machine_condition_data_repository = providers.Factory(
        MachineConditionDataRepository,
        session_factory=db.provided.session
    )
    machine_condition_data_service = providers.Factory(
        MachineConditionDataService,
        repository=machine_condition_data_repository
    )
    
    # Line module providers
    line_repository = providers.Factory(
        LineRepository,
        session_factory=db.provided.session
    )
    line_service = providers.Factory(
        LineService,
        repository=line_repository
    )

    # Maintenance Configuration module providers
    maintenance_configuration_repository = providers.Factory(
        ConfigurationRepository,
        session_factory=db.provided.session
    )
    maintenance_configuration_service = providers.Factory(
        ConfigurationService,
        configuration_repository=maintenance_configuration_repository
    )
    
    # Maintenance LocalStorage module providers
    maintenance_local_storage_repository = providers.Factory(
        LocalStorageRepository,
        session_factory=db.provided.session
    )
    maintenance_local_storage_service = providers.Factory(
        LocalStorageService,
        local_storage_repository=maintenance_local_storage_repository
    )

    def init_resources(self):
        """Initialize resources like database tables."""
        db = self.db()
        db.create_database()