"""Application module."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# First import all models to ensure they are registered with SQLAlchemy Base
from webapp.ADM.TRACKING.failure_group_type.models.failure_group_type_model import FailureGroupType
from webapp.ADM.TRACKING.measurement_data.models.measurement_data_model import MeasurementData
from webapp.IIOT.models.iiot_model import IIOTSensorData
from webapp.ADM.master_data.active_workorder.models.active_workorder_model import ActiveWorkorder
# Other model imports will be added as needed
from .ADM.machine_assets.erp_group.assign_station.endpoints import assign_stations_to_erpgrp_endpoint
from .ADM.machine_assets.erp_group.erp.endpoints import erp_endpoint
from .ADM.machine_assets.machine_setup.cell.endpoints import cell_endpoint
from .ADM.machine_assets.machine_setup.client.endpoints import client_endpoint
from .ADM.machine_assets.machine_setup.company_code.endpoints import company_code_endpoint
from .ADM.machine_assets.machine_setup.machine_group.endpoints import machine_group_endpoint
from .ADM.machine_assets.machine_setup.site.endpoints import site_endpoint
from webapp.ADM.machine_assets.machine_setup.station.endpoints import station_endpoint
from webapp.ADM.machine_assets.machine_setup.user.endpoints import user_endpoint
from .ADM.master_data.part_group.group.endpoints import part_group_endpoint
from .ADM.master_data.part_group.type.endpoints import part_group_type_endpoint
from .ADM.master_data.part_master.endpoints import part_master_endpoint
from .ADM.master_data.part_type.endpoints import part_type_endpoint
from .ADM.master_data.unit.endpoints import unit_endpoint
from .ADM.master_data.workplan_data.workplan.endpoints import workplan_endpoint
from .ADM.master_data.workplan_data.workplan_type.endpoints import workplan_type_endpoint
from .ADM.master_data.workplan_data.worksteps.endpoints import workstep_endpoint
from .ADM.master_data.workorder.endpoints import workorder_endpoint
from .ADM.TRACKING.booking.endpoints.booking_endpoint import router as booking_router
from .ADM.TRACKING.failure_type.endpoints.failure_type_endpoint import router as failure_type_router
from .ADM.TRACKING.failure_group_type.endpoints.failure_group_type_endpoint import router as failure_group_type_router
from .ADM.TRACKING.measurement_data.endpoints.measurement_data_endpoint import router as measurement_data_router
from .IIOT.endpoints.iiot_endpoint import router as iiot_sensor_data_router
from .ADM.MDC.machine_condition_group.endpoints.machine_condition_group_endpoint import router as machine_condition_group_router
from .ADM.MDC.machine_condition.endpoints.machine_condition_endpoint import router as machine_condition_router
from .ADM.MDC.machine_condition_data.endpoints.machine_condition_data_endpoint import router as machine_condition_data_router
from .ADM.bom.endpoints import bom_header_endpoint
from .ADM.bom.endpoints import bom_item_endpoint
from .ADM.master_data.active_workorder.endpoints.active_workorder_endpoint import router as active_workorder_router
from .ADM.maintenance.configuration.endpoints.configuration_endpoint import router as maintenance_configuration_router
from .ADM.maintenance.localStorage.endpoints.local_storage_endpoint import router as maintenance_local_storage_router
from webapp.auth import endpoints as auth_endpoints
# Import container after models but before endpoints
from .containers import Container

def create_app() -> FastAPI:
    """Create FastAPI application."""
    # Create and initialize container first
    container = Container()
    
    # Initialize resources (create database tables)
    container.init_resources()
    
    # Register container providers by name for string-based dependency injection
    # This is done here instead of in containers.py to keep that file clean
    container.providers["failure_group_type_service"] = container.failure_group_type_service
    container.providers["measurement_data_service"] = container.measurement_data_service
    container.providers["active_workorder_service"] = container.active_workorder_service
    
    # Wire the container to modules
    container.wire(modules=[
        "webapp.auth.dependencies",
        "webapp.auth.endpoints",
        "webapp.ADM.machine_assets.machine_setup.user.endpoints.user_endpoint",
        "webapp.ADM.machine_assets.machine_setup.station.endpoints.station_endpoint",
        "webapp.ADM.machine_assets.machine_setup.line.endpoints.line_endpoint",
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
        "webapp.ADM.maintenance.configuration.endpoints.configuration_endpoint",
        "webapp.ADM.maintenance.localStorage.endpoints.local_storage_endpoint",
    ])
    
    app = FastAPI(
        title="MOMES API",
        description="Machine Operations Management and Equipment System API",
        version="1.0.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers - each router should only be included once
    # Do NOT specify tags here as they're already defined in the router
    app.include_router(auth_endpoints.router, prefix="/auth")
    app.include_router(user_endpoint.router, prefix="/users")
    app.include_router(cell_endpoint.router, prefix="/cells")
    app.include_router(client_endpoint.router, prefix="/clients")
    app.include_router(company_code_endpoint.router, prefix="/company-codes")
    app.include_router(site_endpoint.router, prefix="/sites")
    app.include_router(machine_group_endpoint.router, prefix="/machine-groups")
    app.include_router(station_endpoint.router, prefix="/stations")
    # Import and include the line router
    from webapp.ADM.machine_assets.machine_setup.line.endpoints import line_endpoint
    app.include_router(line_endpoint.router, prefix="/lines")
    app.include_router(erp_endpoint.router, prefix="/erp-groups")
    app.include_router(assign_stations_to_erpgrp_endpoint.router, prefix="/assign-stations")
    app.include_router(part_type_endpoint.router, prefix="/part-types")
    app.include_router(part_group_type_endpoint.router, prefix="/part-group-types")
    app.include_router(part_group_endpoint.router, prefix="/part-groups")
    app.include_router(unit_endpoint.router, prefix="/units")
    app.include_router(part_master_endpoint.router, prefix="/part-masters")
    app.include_router(workplan_type_endpoint.router, prefix="/workplan-types")
    app.include_router(workplan_endpoint.router, prefix="/workplans")
    app.include_router(workstep_endpoint.router, prefix="/worksteps")
    app.include_router(workorder_endpoint.router, prefix="/workorders")
    app.include_router(booking_router, prefix="/bookings")
    app.include_router(failure_type_router, prefix="/failure-types")
    app.include_router(failure_group_type_router, prefix="/failure-group-types")
    app.include_router(measurement_data_router, prefix="/measurement-data", tags=["Measurement Data"])
    app.include_router(iiot_sensor_data_router, prefix="/iiot", tags=["IIOT"])
    app.include_router(machine_condition_group_router, prefix="/machine-condition-groups")
    app.include_router(machine_condition_router, prefix="/machine-conditions")
    app.include_router(machine_condition_data_router, prefix="/machine-condition-data")
    app.include_router(bom_header_endpoint.router, prefix="/bom-headers")
    app.include_router(bom_item_endpoint.router, prefix="/bom-items")
    app.include_router(active_workorder_router, prefix="/active-workorders")
    app.include_router(maintenance_configuration_router, prefix="/maintenance/configuration")
    app.include_router(maintenance_local_storage_router, prefix="/maintenance/localStorage")
    
    return app


app = create_app()
