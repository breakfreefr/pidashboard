import requests

STOP_ID = "1401769"  # Ornex, Prénépla

url = f"https://transport.opendata.ch/v1/stationboard?id={STOP_ID}"
data = requests.get(url).json()

for dep in data["stationboard"]:
    destination = dep["to"]

    # Filter only buses going to Cornavin
    if "Cornavin" in destination:
        departure_time = dep["stop"]["departure"]
        delay = dep["stop"]["delay"]

        print(f"{departure_time} | delay: {delay} min")