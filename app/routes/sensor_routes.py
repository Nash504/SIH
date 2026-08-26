from fastapi import APIRouter

from controllers.reading_controller import get_sensors


router = APIRouter(
    prefix="/api/sensors",
    tags=["Sensors"]
)


@router.get("/")
def read_sensors():
    return get_sensors()