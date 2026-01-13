import requests

# ------------------ GEOCODING (PLACE → LAT/LON) ------------------
def geocode_place(place_name):
    """
    Convert place name to latitude & longitude using
    OpenStreetMap Nominatim (FREE).
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "TravelX-AI/1.0 (college-project)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            return None

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon

    except Exception as e:
        print("Geocoding Error:", e)
        return None


# ------------------ ROAD ROUTE (OSRM) ------------------
def get_road_route(source, destination):
    """
    Get road route, distance, time, and geometry between
    source and destination using OSRM (FREE).
    """

    source_coords = geocode_place(source)
    destination_coords = geocode_place(destination)

    if not source_coords or not destination_coords:
        return None

    src_lat, src_lon = source_coords
    dst_lat, dst_lon = destination_coords

    route_url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{src_lon},{src_lat};{dst_lon},{dst_lat}"
        f"?overview=full&geometries=geojson"
    )

    try:
        response = requests.get(route_url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "routes" not in data or not data["routes"]:
            return None

        route = data["routes"][0]

        return {
            "source": {"lat": src_lat, "lon": src_lon},
            "destination": {"lat": dst_lat, "lon": dst_lon},
            "distance_km": round(route["distance"] / 1000, 1),
            "duration_hr": round(route["duration"] / 3600, 1),
            "geometry": route["geometry"]
        }

    except Exception as e:
        print("Route API Error:", e)
        return None
