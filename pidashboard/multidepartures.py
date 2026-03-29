from datetime import datetime

# Sample data (replace with your TPG JSON)
data = {
    "stops": [
        {
            "station_name": "Prévessin-Moëns, mairie",
            "departures": [
                {"number": "66", "to": "Thoiry, Centre commercial", "departure": "2026-03-26T17:52:00+0100", "arrival": "2026-03-26T18:14:00+0100", "platform": "W", "delay": 9},
                {"number": "64", "to": "Ferney, mairie", "departure": "2026-03-26T17:56:00+0100", "arrival": "2026-03-26T18:05:00+0100", "platform": "X", "delay": 0},
            ]
        },
        {
            "station_name": "Ornex, Prénepla",
            "departures": [
                {"number": "64", "to": "Ferney, mairie", "departure": "2026-03-26T18:00:00+0100", "arrival": "2026-03-26T18:10:00+0100", "platform": "Y", "delay": 2},
                {"number": "66", "to": "Thoiry, Centre commercial", "departure": "2026-03-26T18:05:00+0100", "arrival": "2026-03-26T18:25:00+0100", "platform": "Z", "delay": 0},
            ]
        }
    ]
}

def format_time(time_str):
    dt = datetime.fromisoformat(time_str)
    return dt.strftime("%H:%M")

def print_departures_clean(data):
    for stop in data["stops"]:
        station_name = stop["station_name"]
        for dep in stop["departures"]:
            dep_time = format_time(dep["departure"])
            arr_time = format_time(dep["arrival"])
            number = dep["number"]
            destination = dep["to"]
            platform = dep.get("platform", "-")
            delay = dep.get("delay", 0)
            delay_text = f"(+{delay} min)" if delay else ""
            print(f"{station_name} | Bus {number} → {destination} | Dep: {dep_time} {delay_text} | Arr: {arr_time} | Platform: {platform}")

# Run the function
print_departures_clean(data)