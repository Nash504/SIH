from datetime import datetime, timezone

from database.mongodb import get_alerts


from datetime import datetime, timezone

from database.mongodb import get_alerts


def create_alert(sensor_id: str, message: str):
    collection = get_alerts()

    existing_alert = collection.find_one({
        "sensor_id": sensor_id,
        "status": "active"
    })

    if existing_alert:
        return {
            "alert_id": str(existing_alert["_id"]),
            "message": "Existing active alert already exists.",
        }

    alert = {
        "sensor_id": sensor_id,
        "type": "crop_anomaly",
        "message": message,
        "timestamp": datetime.now(timezone.utc),
        "status": "active",
    }

    result = collection.insert_one(alert)

    return {
        "alert_id": str(result.inserted_id),
        "message": "Alert created successfully",
    }