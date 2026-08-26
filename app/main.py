from fastapi import FastAPI

from routes.reading_routes import router as reading_router


app = FastAPI(title="Drishti API")


app.include_router(reading_router) # like app.use("/api/readings", readingRouter);


@app.get("/")
def root():
    return {"message": "Drishti API is running"}