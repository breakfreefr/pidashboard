import requests
from datetime import datetime

def get_departures(stop_name):
    url = "https://transport.opendata.ch/v1/stationboard"
    params = {
        "station": stop_name,
        "limit": 4
    }

    response = requests.get(url, params=params)
    data = response.json()

    departures = []

    for entry in data.get("stationboard", []):
        line = entry.get("number", "?")
        destination = entry.get("to", "?")

        stop_info = entry.get("stop", {})
        departure_time = stop_info.get("departure")

        if departure_time:
            dt = datetime.fromisoformat(departure_time)
            time_str = dt.strftime("%H:%M")
        else:
            time_str = "??:??"

        delay = stop_info.get("delay", 0)
        delay_str = f"+{delay} min" if delay else "on time"

        departures.append(f"{time_str} | {line} → {destination} ({delay_str})")

    return departures


# Example usage
for stop in ["Prévessin-Moëns, mairie","Ornex, Prénepla"]:
    print(stop)
    for dep in get_departures(stop):
        print(dep)