from fastapi import APIRouter

from database.mongodb import get_alerts


router = APIRouter(
    prefix="/api/alerts",
    tags=["Alerts"]
)


@router.get("/")
def get_all_alerts():
    collection = get_alerts()

    alerts = list(
        collection.find().sort("timestamp", -1)
    )

    for alert in alerts:
        alert["_id"] = str(alert["_id"])

    return alerts