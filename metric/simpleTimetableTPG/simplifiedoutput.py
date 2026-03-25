import requests
from datetime import datetime, timezone

URL = "https://transport.opendata.ch/v1/connections"

params = {
    "from": "Prévessin, Prenepla",
    "to": "Genève",
    "limit": 3
}

def parse_time(dt_str):
    # Handles ISO8601 with timezone (e.g. +01:00)
    return datetime.fromisoformat(dt_str)

def main():
    r = requests.get(URL, params=params)
    data = r.json()

    now = datetime.now(timezone.utc)

    for conn in data.get("connections", []):
        dep_str = conn["from"]["departure"]

        dep = parse_time(dep_str)
        dep_utc = dep.astimezone(timezone.utc)

        minutes = int((dep_utc - now).total_seconds() // 60)

        if minutes < 0:
            continue

        # Line number fallback
        line = (
            conn["sections"][0]["journey"]["number"]
            if conn["sections"][0].get("journey")
            else conn["products"][0]
        )

        line = line.replace("Bus ", "")

        time_str = dep.strftime("%H:%M")

        print(f"{line} {time_str} {minutes}m")


if __name__ == "__main__":
    main()
    