from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError
from twilio.base.exceptions import TwilioRestException

from .database import get_sensor_readings
from .schemas import SensorPayload, SmsPayload
from .sms import SmsConfigurationError, send_sms


router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI project initialized with uv!"}


@router.get("/status")
def get_status():
    return {"status": "ok", "project": "sih"}


@router.post("/send", status_code=201)
def receive_sensor_reading(payload: SensorPayload | None = None):
    reading = payload or SensorPayload(
        b1={"temp": 24.5, "humidity": 61.2},
        b2={"temp": 24.7, "humidity": 60.8},
        b3={"temp": 24.4, "humidity": 62.0},
        timestamp=datetime.now(timezone.utc),
        sensor_id="dummy-sensor",
    )
    try:
        result = get_sensor_readings().insert_one(reading.model_dump())
        return {
            "status": "stored",
            "id": str(result.inserted_id),
            "sensor_id": reading.sensor_id,
        }
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Could not store sensor reading") from exc


@router.post("/send-sms", status_code=201)
def send_sms_message(payload: SmsPayload):
    try:
        message_id = send_sms(payload.phone_number, payload.message)
        return {"status": "sent", "id": message_id}
    except SmsConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except TwilioRestException as exc:
        detail = exc.msg or "Could not send SMS"
        if exc.code:
            detail = f"Twilio error {exc.code}: {detail}"
        raise HTTPException(status_code=502, detail=detail) from exc