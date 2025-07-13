from fastapi import APIRouter, HTTPException
from app.models import SensorData, Alert
from app.db import db
from app.logic import is_within_geofence, check_tampering
from app.alerts import send_email_alert
from datetime import datetime
from bson import ObjectId  # For ObjectId type

router = APIRouter()

# ✅ Helper: Convert ObjectId to string
def fix_objectid(doc):
    """Convert MongoDB _id ObjectId to string"""
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("/ingest")
async def ingest_data(data: SensorData):
    truck = await db.vehicles.find_one({"truck_id": data.truck_id})
    
    # Geofence check
    inside_fence = is_within_geofence(data.latitude, data.longitude)
    alert_messages = []

    # Tampering check
    if truck:
        last_level = truck['fuel_level']
        last_timestamp = truck.get('timestamp')
        if last_timestamp:
            time_diff = (datetime.utcnow() - last_timestamp).total_seconds() / 60
        else:
            time_diff = 0

        if check_tampering(data.fuel_level, last_level, time_diff):
            alert_messages.append("Tampering detected: sudden fuel drop!")

    if not inside_fence:
        alert_messages.append("Geofence breach detected!")

    # Save latest vehicle data
    await db.vehicles.update_one(
        {"truck_id": data.truck_id},
        {"$set": data.dict()},
        upsert=True
    )

    # Save alerts + send emails
    for msg in alert_messages:
        alert_doc = Alert(
            truck_id=data.truck_id,
            message=msg,
            timestamp=datetime.utcnow()
        ).dict()
        await db.alerts.insert_one(alert_doc)

        # ✅ Send email immediately
        send_email_alert(
            subject=f"ALERT: {msg}",
            body=f"""
Truck ID: {data.truck_id}
Message: {msg}
Latitude: {data.latitude}
Longitude: {data.longitude}
Timestamp: {datetime.utcnow()}
"""
        )

    return {"status": "success", "alerts": alert_messages}

@router.get("/dashboard-data")
async def get_dashboard_data():
    try:
        vehicles = await db.vehicles.find().to_list(100)
        alerts = await db.alerts.find().sort("timestamp", -1).limit(10).to_list(10)

        # ✅ Fix ObjectId before returning
        vehicles = [fix_objectid(v) for v in vehicles]
        alerts = [fix_objectid(a) for a in alerts]

        return {
            "vehicles": vehicles,
            "alerts": alerts
        }
    except Exception as e:
        return {"error": str(e)}
