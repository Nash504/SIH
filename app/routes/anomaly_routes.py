from fastapi import APIRouter

from controllers.anomaly_controller import check_anomaly


router = APIRouter(
    prefix="/api/anomaly",
    tags=["Anomaly Detection"]
)


@router.get("/")
def detect_anomaly():
    return check_anomaly()