# Fuel-truck-monitoring
IoT Fuel Truck Monitoring System with FastAPI, MongoDB, and Live Map Dashboard

# 🚚 Fuel Truck Monitoring System

**Description:**  
IoT Fuel Truck Monitoring System using **FastAPI**, **MongoDB**, **Leaflet.js**, and **SMTP email alerts**.  
Features:
- Geofence detection
- Tampering alerts
- Live dashboard with map
- Email notifications for events

## ⚙️ How to Run
1. Create `.env` file with your Mongo URI and SMTP details.
2. Run the FastAPI backend:  
   ```bash
   uvicorn app.main:app --reload
