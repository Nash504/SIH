from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SensorReading(BaseModel):
    temp: float
    humidity: float


class SensorPayload(BaseModel):
    b1: SensorReading
    b2: SensorReading
    b3: SensorReading
    timestamp: datetime
    sensor_id: str = Field(min_length=1)


class SmsPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")
    message: str = Field(
        min_length=1,
        max_length=1600,
        examples=["Alert: check crops."],
        description="The alert text to send to the phone number.",
    )