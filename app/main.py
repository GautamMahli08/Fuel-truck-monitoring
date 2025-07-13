from fastapi import FastAPI
from app.routes import router
import uvicorn
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Fuel Truck Monitoring System",
    description="Ingests fuel level & GPS data, detects tampering & geofence breaches",
    version="1.0"
)

# Include all your routes
app.include_router(router)
# ✅ Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
