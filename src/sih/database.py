import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection


load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "sih")

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)


def get_sensor_readings() -> Collection:
    return client[MONGODB_DATABASE]["sensor_readings"]


def close_client() -> None:
    client.close()