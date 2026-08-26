from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SensorReading(BaseModel):
    temp: float
    humidity: float
    gas: float
    heat_Index: float


class SensorPayload(BaseModel):
    sensor_id: str = Field(min_length=1)
    timestamp: datetime
    reading: SensorReading

"""
This is what is gonna get sent to the API endpoint. Example:
{
    "sensor_id": "S2",
    "timestamp": "2026-08-26T17:30:00",
    "reading": {
        "temp": 32.4,
        "humidity": 71.2,
        "gas": 50.0,
        "heat_Index": 35.6
    }
}
"""

class SmsPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")
    message: str = Field(
        min_length=1,
        max_length=1600,
        examples=["Alert: check crops."],
        description="The alert text to send to the phone number.",
    )