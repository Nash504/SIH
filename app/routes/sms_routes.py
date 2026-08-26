from fastapi import APIRouter

from controllers.sms_controller import send_sms
from models.sensor import SmsPayload


router = APIRouter(
    prefix="/api/sms",
    tags=["SMS"]
)


@router.post("/")
def send_sms_notification(payload: SmsPayload):
    return send_sms(payload)