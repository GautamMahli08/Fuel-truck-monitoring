# simulator.py
import requests
import random
from time import sleep

url = "http://localhost:8000/ingest"

truck_ids = ["TRUCK-101", "TRUCK-102"]

while True:
    data = {
        "truck_id": random.choice(truck_ids),
        "latitude": 23.5859 + random.uniform(-0.01, 0.01),
        "longitude": 58.4059 + random.uniform(-0.01, 0.01),
        "fuel_level": random.randint(40, 100)
    }
    r = requests.post(url, json=data)
    print(r.json())
    sleep(5)  # every 5 seconds
