from database.mongodb import get_sensor_readings


TEMP_THRESHOLD = 2.0
HUMIDITY_THRESHOLD = 5.0
GAS_THRESHOLD = 10.0
HEAT_INDEX_THRESHOLD = 2.0


def check_anomaly():
    collection = get_sensor_readings()

    sensors = collection.distinct("sensor_id")

    if len(sensors) < 3:
        return {
            "anomaly": False,
            "message": "At least 3 sensors are required."
        }

    latest_readings = {}

    for sensor_id in sensors:
        reading = collection.find_one(
            {"sensor_id": sensor_id},
            sort=[("timestamp", -1)]
        )

        if reading:
            latest_readings[sensor_id] = reading

    if len(latest_readings) < 3:
        return {
            "anomaly": False,
            "message": "Not enough sensor readings."
        }

    sensors_list = list(latest_readings.items())

    anomalies = []

    for sensor_id, reading in sensors_list:
        other_readings = [
            other_reading
            for other_id, other_reading in sensors_list
            if other_id != sensor_id
        ]

        avg_temp = sum(
            r["temp"] for r in other_readings
        ) / len(other_readings)

        avg_humidity = sum(
            r["humidity"] for r in other_readings
        ) / len(other_readings)

        avg_gas = sum(
            r["gas"] for r in other_readings
        ) / len(other_readings)

        avg_heat_index = sum(
            r["heatIndex"] for r in other_readings
        ) / len(other_readings)

        if (
            abs(reading["temp"] - avg_temp) > TEMP_THRESHOLD
            or abs(reading["humidity"] - avg_humidity) > HUMIDITY_THRESHOLD
            or abs(reading["gas"] - avg_gas) > GAS_THRESHOLD
            or abs(reading["heatIndex"] - avg_heat_index) > HEAT_INDEX_THRESHOLD
        ):
            anomalies.append({
                "sensor_id": sensor_id,
                "temperature": reading["temp"],
                "humidity": reading["humidity"],
                "gas": reading["gas"],
                "heatIndex": reading["heatIndex"]
            })

    if anomalies:
        return {
            "anomaly": True,
            "message": "Potential anomaly detected.",
            "sensors": anomalies
        }

    return {
        "anomaly": False,
        "message": "All sensors are within normal range."
    }