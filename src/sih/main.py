import os
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from pymongo.errors import PyMongoError


class SensorReading(BaseModel):
    temp: float
    humidity: float


class SensorPayload(BaseModel):
    b1: SensorReading
    b2: SensorReading
    b3: SensorReading
    timestamp: datetime
    sensor_id: str = Field(min_length=1)


def get_collection():
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
    database = client[os.getenv("MONGODB_DATABASE", "sih")]
    return client, database["sensor_readings"]

app = FastAPI(title="SIH Project API", version="0.1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI project initialized with uv!"}

@app.get("/status")
def get_status():
    return {"status": "ok", "project": "sih"}


@app.post("/send", status_code=201)
def receive_sensor_reading(payload: SensorPayload):
    client, collection = get_collection()
    try:
        result = collection.insert_one(payload.model_dump())
        return {"status": "stored", "id": str(result.inserted_id)}
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Could not store sensor reading") from exc
    finally:
        client.close()
