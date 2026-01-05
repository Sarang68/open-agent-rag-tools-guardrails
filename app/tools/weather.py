import re
import requests

def get_current_weather(city: str, units: str = "celsius") -> dict:
    # Remove trailing punctuation and extra whitespace
    city = city.strip()
    city = re.sub(r"[^\w\s,.-]", "", city).strip()  # removes ?, !, quotes, etc.

    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},
        timeout=20,
    ).json()

    if not geo.get("results"):
        return {"error": f"City not found: {city}"}

    loc = geo["results"][0]
    lat, lon = loc["latitude"], loc["longitude"]

    forecast = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "temperature_unit": "celsius" if units.lower().startswith("c") else "fahrenheit",
        },
        timeout=20,
    ).json()

    cw = forecast.get("current_weather", {})
    return {
        "city": city,
        "latitude": lat,
        "longitude": lon,
        "temperature": cw.get("temperature"),
        "windspeed": cw.get("windspeed"),
        "time": cw.get("time"),
        "units": units,
    }

