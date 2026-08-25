from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo.errors import PyMongoError

load_dotenv()

from .database import close_client, client
from .routes import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        client.admin.command("ping")
    except PyMongoError as exc:
        raise RuntimeError("Could not connect to MongoDB") from exc
    yield
    close_client()

app = FastAPI(title="SIH Project API", version="0.1.0", lifespan=lifespan)
app.include_router(router)
