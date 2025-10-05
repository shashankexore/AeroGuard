import os
import requests
import pandas as pd
from datetime import datetime, timezone

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_airnow_by_latlon(lat, lon):
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": API_KEY}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    j = r.json()
    items = j.get("list", [])
    rows = []
    for it in items:
        ts = it.get("dt")
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        comps = it.get("components", {})
        rows.append({
            "DateObserved": dt,
            "pm2_5": comps.get("pm2_5"),
            "pm10": comps.get("pm10"),
            "no2": comps.get("no2"),
            "o3": comps.get("o3"),
            "co": comps.get("co"),
            "so2": comps.get("so2"),
            "nh3": comps.get("nh3"),
            "main_aqi": it.get("main", {}).get("aqi"),
            "Latitude": lat,
            "Longitude": lon
        })
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    print(get_airnow_by_latlon(40.7128, -74.0060).head().to_dict())
