from models.sensor import SensorPayload
from database.mongodb import get_sensor_readings


def create_reading(payload: SensorPayload): # req body must follow the pydantic model defined in models/sensor.py
    collection = get_sensor_readings() # get the collection from the database i.e. sensor_readings collection in the sih database

    reading = {
        "sensor_id": payload.sensor_id,
        "timestamp": payload.timestamp,
        "temp": payload.reading.temp,
        "humidity": payload.reading.humidity,
        "gas": payload.reading.gas,
        "heat_Index": payload.reading.heatIndex,
    }

    result = collection.insert_one(reading) # easy way of performing operations coz of first line of code in this function. we can directly use the collection object to perform operations on the collection. here we are inserting a document into the collection.

    return {
        "message": "Reading stored successfully",
        "id": str(result.inserted_id),
    } # Pydantic + FastAPI are already handling request validation.

"""
INPUT:
{
  "sensor_id": "S2",
  "timestamp": "2026-08-26T17:30:00",
  "reading": {
    "temp": 32.4,
    "humidity": 71.2,
    "gas": 50.0,
    "heatIndex": 35.6
  }
}
"""

def get_all_readings():
    collection = get_sensor_readings()

    readings = list(collection.find().sort("timestamp", -1))

    for reading in readings:
        reading["_id"] = str(reading["_id"])

    return readings

def get_readings_by_sensor(sensor_id: str):
    collection = get_sensor_readings()

    readings = list(
        collection.find(
            {"sensor_id": sensor_id}
        ).sort("timestamp", -1)
    )

    for reading in readings:
        reading["_id"] = str(reading["_id"])

    return readings