from geopy.distance import geodesic

# Example: center of your allowed area
GEOFENCE_CENTER = (23.5859, 58.4059)  # Muscat coordinates (example)
GEOFENCE_RADIUS_KM = 5  # 5 km radius

def is_within_geofence(lat, lon):
    distance = geodesic(GEOFENCE_CENTER, (lat, lon)).km
    return distance <= GEOFENCE_RADIUS_KM

def check_tampering(current_level, last_level, time_diff_minutes=5):
    # Example: if fuel drops by >10% in 5 min
    if last_level == 0:
        return False
    drop_percent = ((last_level - current_level) / last_level) * 100
    return drop_percent > 10
