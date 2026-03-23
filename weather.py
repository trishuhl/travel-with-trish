import re
import requests
from datetime import date, timedelta


WMO_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}


def geocode(destination: str) -> tuple[float, float, str]:
    """Return (latitude, longitude, resolved_name) for a destination string."""
    resp = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": destination, "count": 1, "language": "en", "format": "json"},
        timeout=10,
    )
    resp.raise_for_status()
    results = resp.json().get("results")
    if not results:
        raise ValueError(f"Could not geocode destination: {destination!r}")
    r = results[0]
    name = f"{r['name']}, {r.get('country', '')}"
    return r["latitude"], r["longitude"], name


def parse_dates(dates_str: str) -> tuple[date, date]:
    """Parse a date range like 'June 10-17' or 'July 4-11, 2025'."""
    today = date.today()

    # Try to extract a year
    year_match = re.search(r"\b(20\d{2})\b", dates_str)
    year = int(year_match.group(1)) if year_match else today.year

    # Remove the year from the string for further parsing
    clean = re.sub(r",?\s*20\d{2}", "", dates_str).strip()

    # Match "Month start-end" e.g. "June 10-17"
    m = re.match(r"([A-Za-z]+)\s+(\d+)-(\d+)", clean)
    if m:
        month_str, start_day, end_day = m.groups()
        month = _month_num(month_str)
        start = date(year, month, int(start_day))
        end = date(year, month, int(end_day))
        return start, end

    # Match "Month start - Month end" e.g. "June 28 - July 5"
    m = re.match(r"([A-Za-z]+)\s+(\d+)\s*-\s*([A-Za-z]+)\s+(\d+)", clean)
    if m:
        m1, d1, m2, d2 = m.groups()
        start = date(year, _month_num(m1), int(d1))
        end = date(year, _month_num(m2), int(d2))
        return start, end

    raise ValueError(f"Could not parse dates: {dates_str!r}")


def _month_num(name: str) -> int:
    months = ["january","february","march","april","may","june",
              "july","august","september","october","november","december"]
    name = name.lower()
    for i, m in enumerate(months, 1):
        if m.startswith(name[:3]):
            return i
    raise ValueError(f"Unknown month: {name!r}")


def get_forecast(destination: str, dates_str: str) -> dict:
    """Fetch weather forecast and return a summary dict."""
    lat, lon, resolved_name = geocode(destination)
    start, end = parse_dates(dates_str)

    # Open-Meteo caps forecasts at 16 days; clamp end date
    max_end = date.today() + timedelta(days=15)
    if end > max_end:
        end = max_end

    resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode",
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "timezone": "auto",
        },
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()["daily"]

    temps_max = data["temperature_2m_max"]
    temps_min = data["temperature_2m_min"]
    precip = data["precipitation_probability_max"]
    codes = data["weathercode"]

    descriptions = [WMO_DESCRIPTIONS.get(c, "Unknown") for c in codes]

    return {
        "destination": resolved_name,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "temp_max_c": round(max(temps_max), 1),
        "temp_min_c": round(min(temps_min), 1),
        "avg_temp_c": round(sum(temps_max) / len(temps_max), 1),
        "max_precip_pct": max(precip),
        "conditions": list(set(descriptions)),
        "daily": [
            {
                "date": data["time"][i],
                "temp_max": temps_max[i],
                "temp_min": temps_min[i],
                "precip_pct": precip[i],
                "condition": descriptions[i],
            }
            for i in range(len(data["time"]))
        ],
    }
