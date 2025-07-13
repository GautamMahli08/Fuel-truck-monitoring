from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SensorData(BaseModel):
    truck_id: str
    fuel_level: float  # in liters
    latitude: float
    longitude: float
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Alert(BaseModel):
    truck_id: str
    message: str
    timestamp: datetime
