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
        "heatIndex": payload.reading.heatIndex,
    }

    result = collection.insert_one(reading) # easy way of performing operations coz of first line of code in this function. we can directly use the collection object to perform operations on the collection. here we are inserting a document into the collection.

    return {
        "message": "Reading stored successfully",
        "id": str(result.inserted_id),
    } # Pydantic + FastAPI are already handling request validation.