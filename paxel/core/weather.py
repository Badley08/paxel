"""
Je récupère ici les données météo via le service wttr.in.
C'est simple, gratuit et ne nécessite pas de clé API.
"""

import urllib.request
import urllib.parse
import urllib.error
import json


def get_weather(city: str = "") -> str:
    """
    Je récupère la météo actuelle via wttr.in.
    Si aucune ville n'est fournie, wttr.in utilise la localisation IP.
    """
    try:
        if city:
            city_encoded = urllib.parse.quote(city)
            url = f"https://wttr.in/{city_encoded}?format=j1&lang=fr"
        else:
            url = "https://wttr.in/?format=j1&lang=fr"

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Paxel/0.1 (Linux assistant)"}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        return _parse_weather_data(data, city)

    except urllib.error.URLError:
        return "❌ Impossible de récupérer la météo. Vérifie ta connexion internet."
    except json.JSONDecodeError:
        return "❌ Erreur lors de la lecture des données météo."
    except Exception as e:
        return f"❌ Erreur météo : {e}"


def _parse_weather_data(data: dict, city: str = "") -> str:
    """Je parse et formate les données météo reçues de wttr.in."""
    try:
        current = data["current_condition"][0]
        nearest_area = data["nearest_area"][0]

        location_name = nearest_area["areaName"][0]["value"]
        country = nearest_area["country"][0]["value"]

        temp_c = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        wind_speed = current["windspeedKmph"]
        wind_dir = current["winddir16Point"]
        description = current["lang_fr"][0]["value"] if current.get("lang_fr") else current["weatherDesc"][0]["value"]

        weather_emoji = _get_weather_emoji(description)

        return (
            f"{weather_emoji} {description}\n"
            f"📍 {location_name}, {country}\n"
            f"🌡️  Température : {temp_c}°C (ressenti {feels_like}°C)\n"
            f"💧 Humidité : {humidity}%\n"
            f"💨 Vent : {wind_speed} km/h {wind_dir}"
        )
    except (KeyError, IndexError) as e:
        return f"❌ Impossible de lire les données météo : {e}"


def _get_weather_emoji(description: str) -> str:
    """Je retourne un emoji correspondant aux conditions météo."""
    desc_lower = description.lower()
    if any(w in desc_lower for w in ["soleil", "clair", "dégagé", "sunny", "clear"]):
        return "☀️"
    elif any(w in desc_lower for w in ["nuageux", "couvert", "overcast", "cloudy"]):
        return "☁️"
    elif any(w in desc_lower for w in ["pluie", "rain", "pluvieux", "averse"]):
        return "🌧️"
    elif any(w in desc_lower for w in ["orage", "thunder", "storm"]):
        return "⛈️"
    elif any(w in desc_lower for w in ["neige", "snow"]):
        return "❄️"
    elif any(w in desc_lower for w in ["brouillard", "fog", "brume"]):
        return "🌫️"
    elif any(w in desc_lower for w in ["partiellement", "partly"]):
        return "⛅"
    else:
        return "🌤️"
