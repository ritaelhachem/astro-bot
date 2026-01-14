import requests

PLANET_DATA = {
    "mercury": {"distance_from_sun_km": 57900000, "orbital_period_days": 88},
    "venus": {"distance_from_sun_km": 108200000, "orbital_period_days": 225},
    "earth": {"distance_from_sun_km": 149600000, "orbital_period_days": 365},
    "mars": {"distance_from_sun_km": 227900000, "orbital_period_days": 687},
    "jupiter": {"distance_from_sun_km": 778500000, "orbital_period_days": 4333},
    "saturn": {"distance_from_sun_km": 1433000000, "orbital_period_days": 10759},
    "uranus": {"distance_from_sun_km": 2877000000, "orbital_period_days": 30687},
    "neptune": {"distance_from_sun_km": 4503000000, "orbital_period_days": 60190}
}

ISS_API = "http://api.open-notify.org/iss-now.json"


def celestial_position(object_name: str):

    name = object_name.lower().strip()

    if name in ["iss", "station spatiale internationale"]:
        try:
            response = requests.get(ISS_API, timeout=10)
            response.raise_for_status()
            data = response.json()

            position = data.get("iss_position", {})
            return {
                "object": "ISS",
                "type": "satellite",
                "latitude": position.get("latitude"),
                "longitude": position.get("longitude"),
                "source": "Open Notify API"
            }

        except Exception as e:
            print(f"Erreur API ISS: {e}")
            return {"error": "Impossible de récupérer la position de l'ISS."}

    if name in PLANET_DATA:
        info = PLANET_DATA[name]
        return {
            "object": name.capitalize(),
            "type": "planet",
            "distance_from_sun_km": info["distance_from_sun_km"],
            "orbital_period_days": info["orbital_period_days"],
            "source": "Internal astronomy database"
        }

    return {"error": f"Objet céleste inconnu : {object_name}"}
