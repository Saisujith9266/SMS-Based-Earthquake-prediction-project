from math import radians, sin, cos, sqrt, atan2

EARTH_RADIUS_KM = 6371.0088

def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = radians(lat1), radians(lat2)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(p1) * cos(p2) * sin(dlon / 2) ** 2
    return EARTH_RADIUS_KM * 2 * atan2(sqrt(a), sqrt(1 - a))

def is_within_radius(event_lat, event_lon, user_lat, user_lon, radius_km):
    return haversine_km(event_lat, event_lon, user_lat, user_lon) <= radius_km
