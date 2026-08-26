from fastapi import APIRouter

from controllers.reading_controller import (
    create_reading,
    get_all_readings,
    get_readings_by_sensor,
)
from models.sensor import SensorPayload


router = APIRouter(
    prefix="/api/readings",
    tags=["Readings"]
)


@router.post("/")
def add_reading(payload: SensorPayload):
    return create_reading(payload)


@router.get("/")
def read_readings():
    return get_all_readings()


@router.get("/{sensor_id}")
def read_sensor_readings(sensor_id: str):
    return get_readings_by_sensor(sensor_id)