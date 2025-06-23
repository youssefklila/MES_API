from fastapi import APIRouter, Depends, HTTPException, Security, Query
from dependency_injector.wiring import inject, Provide
from IIOT.containers import Container
from IIOT.iot.schemas import SensorData, SensorDataResponse
from IIOT.iot.service import IoTService
from IIOT.auth.dependencies import get_current_user, permission_required
from fastapi.security import OAuth2PasswordBearer
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(
    tags=["IoT"],
    prefix="/iot",
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/subscribe",
    response_model=SensorDataResponse,
    summary="Subscribe to sensor data",
    description="Retrieves the latest sensor data from the MQTT broker"
)
@inject
async def subscribe_to_sensor_data(
    topic: Optional[str] = Query(None, description="MQTT topic to subscribe to"),
    current_user: dict = Depends(permission_required("iot:subscribe")),
    iot_service: IoTService = Depends(Provide[Container.iot_service]),
    token: str = Security(oauth2_scheme)
):
    """Subscribe to sensor data from MQTT
    
    Args:
        topic: Optional MQTT topic to subscribe to. If not provided, the default topic will be used.
    """
    try:
        logger.info(f"GET /iot/subscribe - Retrieving sensor data{' from topic ' + topic if topic else ''}")
        data = iot_service.get_sensor_data(topic)
    except Exception as e:
        logger.error(f"GET /iot/subscribe - Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    if not data:
        logger.warning(f"No sensor data found for topic: {topic}")
        raise HTTPException(status_code=404, detail=f"No sensor data found for topic: {topic}")
    logger.info(f"GET /iot/subscribe - Success: {data}")
    return data

@router.post(
    "/publish",
    summary="Publish sensor data",
    description="Publish and process sensor data to MQTT broker"
)
@inject
async def publish_sensor_data(
    data: SensorData,
    current_user: dict = Depends(permission_required("iot:publish")),
    iot_service: IoTService = Depends(Provide[Container.iot_service]),
    token: str = Security(oauth2_scheme)
):
    """Publish sensor data to MQTT broker
    
    Args:
        data: Sensor data to publish, including an optional topic field
    """
    try:
        logger.info(f"POST /iot/publish - Received data: {data.dict()}")
        topic = data.topic
        data_dict = data.dict()
        if "topic" in data_dict:
            data_dict.pop("topic")
        processed = iot_service.process_sensor_data(data_dict, topic)
        logger.info(f"POST /iot/publish - Success: {processed}")
        return {"status": "success", "data": processed}
    except Exception as e:
        logger.error(f"POST /iot/publish - Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
