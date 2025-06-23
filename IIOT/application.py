"""Application module."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from IIOT.ADM.machine_assets.machine_setup.user.endpoints import user_endpoint
from IIOT.containers import Container
from IIOT.auth import endpoints as auth_endpoints
from IIOT.iot import endpoints as iot_endpoints
from IIOT.monitoring.tasks.endpoints import task_router
from IIOT.monitoring.reports.endpoints import report_router
import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response with status code
        status_code = response.status_code
        status_color = "\033[92m" if status_code < 400 else "\033[91m"  # Green for success, red for error
        logger.info(f"{status_color}{request.method} {request.url.path} - Status: {status_code} - Time: {process_time:.2f}s\033[0m")
        
        return response

def create_app() -> FastAPI:
    """Create FastAPI application."""
    container = Container()
    container.init_resources()
    
    app = FastAPI(
        title="IIOT API",
        version="1.0.0",
        description="Integrated API with Authentication, User Management and IoT capabilities"
    )
    
    # Add logging middleware
    app.add_middleware(LoggingMiddleware)
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Wire containers - specify exact packages that need wiring
    logger.debug("Wiring containers...")
    container.wire(
        packages=[
            "IIOT.auth",
            "IIOT.ADM.machine_assets.machine_setup.user",
            "IIOT.iot",
            "IIOT.monitoring.tasks",
            "IIOT.monitoring.reports"
        ]
    )
    
    # Include routers
    logger.debug("Including routers...")
    app.include_router(auth_endpoints.router, prefix="/auth", tags=["Authentication"])
    app.include_router(user_endpoint.router, prefix="/users", tags=["Users"])
    app.include_router(iot_endpoints.router, prefix="/iot", tags=["IoT"])
    app.include_router(task_router, prefix="/monitoring/tasks", tags=["Tasks"])
    app.include_router(report_router, prefix="/monitoring/reports", tags=["Reports"])
    
    # Log all registered routes
    logger.debug("Registered routes:")
    for route in app.routes:
        route_tags = getattr(route, 'tags', [])
        logger.debug(f"Route: {route.path} - Tags: {route_tags}")
    
    # Start MQTT client on application startup
    @app.on_event("startup")
    async def startup_event():
        logger.debug("Starting MQTT client...")
        container.mqtt_client().start()
        logger.debug("MQTT client started")
    
    return app

app = create_app()