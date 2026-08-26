from fastapi import APIRouter

from controllers.reading_controller import create_reading
from models.sensor import SensorPayload


router = APIRouter(
    prefix="/api/readings",
    tags=["Readings"] # for swagger
)


@router.post("/")
def add_reading(payload: SensorPayload):
    return create_reading(payload)