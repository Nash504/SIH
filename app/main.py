from fastapi import FastAPI

from routes.reading_routes import router as reading_router
from routes.sensor_routes import router as sensor_router
from routes.anomaly_routes import router as anomaly_router


app = FastAPI(title="Drishti API")

app.include_router(sensor_router)
app.include_router(reading_router) # like app.use("/api/readings", readingRouter);
app.include_router(anomaly_router)

@app.get("/")
def root():
    return {"message": "Drishti API is running"}