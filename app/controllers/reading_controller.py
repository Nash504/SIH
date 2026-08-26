from models.sensor import SensorPayload
from database.mongodb import get_sensor_readings
from controllers.anomaly_controller import check_anomaly


def create_reading(payload: SensorPayload):
    collection = get_sensor_readings()

    reading = {
        "sensor_id": payload.sensor_id,
        "timestamp": payload.timestamp,
        "temp": payload.reading.temp,
        "humidity": payload.reading.humidity,
        "gas": payload.reading.gas,
        "heatIndex": payload.reading.heatIndex,
    }

    result = collection.insert_one(reading)

    anomaly_result = check_anomaly()

    return {
        "message": "Reading stored successfully",
        "id": str(result.inserted_id),
        "anomaly": anomaly_result,
    }


def get_all_readings():
    collection = get_sensor_readings()

    readings = list(
        collection.find().sort("timestamp", -1)
    )

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


def get_sensors():
    collection = get_sensor_readings()

    sensors = collection.distinct("sensor_id")

    return [
        {
            "sensor_id": sensor_id
        }
        for sensor_id in sensors
    ]