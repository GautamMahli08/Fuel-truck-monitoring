import requests
import random
from time import sleep
from datetime import datetime

URL = "http://localhost:8000/ingest"

# 10 trucks with initial fuel and route index
TRUCKS = {
    f"TRUCK-{i:03d}": {"fuel_level": random.uniform(70, 100), "route_index": 0}
    for i in range(101, 111)
}

# Example route: simple circle of 5 GPS points near Muscat
ROUTE = [
    (23.5859, 58.4059),
    (23.5865, 58.4070),
    (23.5870, 58.4080),
    (23.5860, 58.4090),
    (23.5850, 58.4100),
]

print("🚚 Realistic IoT Simulator started! Sending data for 10 trucks...")

while True:
    truck_id = random.choice(list(TRUCKS.keys()))
    truck = TRUCKS[truck_id]

    # Normal fuel usage: slight decrease
    truck["fuel_level"] -= random.uniform(0.05, 0.3)

    # Simulate tampering: sudden drop with small chance
    if random.random() < 0.05:  # 5% chance
        drop = random.uniform(5, 15)
        truck["fuel_level"] -= drop
        print(f"🚨 Tampering simulated for {truck_id}! Fuel dropped by {drop:.2f} liters.")

    # Refuel if empty
    if truck["fuel_level"] < 10:
        truck["fuel_level"] = random.uniform(70, 100)
        print(f"⛽ {truck_id} refueled to {truck['fuel_level']:.2f} liters.")

    # Get current route point
    lat, lon = ROUTE[truck["route_index"]]
    truck["route_index"] = (truck["route_index"] + 1) % len(ROUTE)

    # 10% chance: push position out of geofence
    if random.random() < 0.1:
        lat += 0.05
        lon += 0.05
        print(f"⚠️ Geofence breach simulated for {truck_id}!")

    payload = {
        "truck_id": truck_id,
        "latitude": lat + random.uniform(-0.0005, 0.0005),  # Tiny jitter
        "longitude": lon + random.uniform(-0.0005, 0.0005),
        "fuel_level": round(truck["fuel_level"], 2)
    }

    response = requests.post(URL, json=payload)

    print(
        f"[{datetime.utcnow()}] {truck_id} | Fuel: {payload['fuel_level']:.2f} | "
        f"Geo: ({payload['latitude']:.5f}, {payload['longitude']:.5f}) | Response: {response.json()}"
    )

    sleep(random.uniform(2, 5))  # Variable delay for realism
