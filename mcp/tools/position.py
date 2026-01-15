from __future__ import annotations

import unicodedata
from datetime import datetime, timezone
from typing import Optional, Dict, Any

import requests
from skyfield.api import load, Topos


OBJECTS_FR = {
    "soleil": "sun",
    "lune": "moon",
    "mercure": "mercury",
    "venus": "venus",
    "mars": "mars",
    "jupiter": "jupiter barycenter",
    "saturne": "saturn barycenter",
    "uranus": "uranus barycenter",
    "neptune": "neptune barycenter",
}

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def normalize(text: str) -> str:
    """Minuscule + suppression accents + trim."""
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def azimuth_to_direction(az: float) -> str:
    """Convertit l'azimut en direction cardinale approximative."""
    directions = ["Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest"]
    return directions[round(az / 45) % 8]


def parse_time(iso_time: Optional[str]) -> datetime:
    """None => maintenant UTC ; sinon ISO '2026-01-09T20:30:00Z' ou +00:00."""
    if not iso_time:
        return datetime.now(timezone.utc)
    return datetime.fromisoformat(iso_time.replace("Z", "+00:00")).astimezone(timezone.utc)


def geocode_location(query: str) -> Dict[str, Any]:
    """
    Transforme une ville/pays en lat/lon via Nominatim (OpenStreetMap).
    """
    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "AstroBot-Hephaestus/1.0 (student project)"
    }

    r = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=15)
    r.raise_for_status()
    data = r.json()

    if not data:
        return {"error": f"Localisation introuvable: {query}"}

    first = data[0]
    return {
        "display_name": first.get("display_name", query),
        "lat": float(first["lat"]),
        "lon": float(first["lon"]),
        "source": "Nominatim (OpenStreetMap)"
    }


def celestial_visibility_by_latlon(object_name: str, lat: float, lon: float, iso_time: Optional[str] = None) -> Dict[str, Any]:
    """
    Calcule la visibilité d'un astre depuis lat/lon avec Skyfield.
    """
    name = normalize(object_name)

    if name not in OBJECTS_FR:
        return {
            "error": f"Objet céleste inconnu : {object_name}",
            "objets_supportes": sorted(list(OBJECTS_FR.keys()))
        }

    dt = parse_time(iso_time)

    ts = load.timescale()
    eph = load("de421.bsp")  

    earth = eph["earth"]
    body = eph[OBJECTS_FR[name]]

    t = ts.from_datetime(dt)
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)

    astrometric = observer.at(t).observe(body)
    alt, az, _ = astrometric.apparent().altaz()

    altitude = float(alt.degrees)
    azimuth = float(az.degrees)

    return {
        "objet": object_name.capitalize(),
        "heure_utc": dt.isoformat().replace("+00:00", "Z"),
        "visible": altitude > 0,
        "altitude_deg": round(altitude, 2),
        "azimuth_deg": round(azimuth, 2),
        "direction": azimuth_to_direction(azimuth),
        "source": "Skyfield (de421.bsp)"
    }


def celestial_position(object_name: str, location: str, iso_time: Optional[str] = None) -> Dict[str, Any]:
    """
    Tool principal :
    - prend un objet (ex: 'mars')
    - prend une localisation (ex: 'Paris' ou 'Beyrouth, Liban')
    - retourne visibilité + direction + altitude
    """

    geo = geocode_location(location)
    if "error" in geo:
        return geo

    lat = geo["lat"]
    lon = geo["lon"]

    vis = celestial_visibility_by_latlon(object_name, lat, lon, iso_time)

    return {
        "location": {
            "query": location,
            "display_name": geo.get("display_name", location),
            "lat": lat,
            "lon": lon,
            "source": geo.get("source")
        },
        "result": vis
    }
