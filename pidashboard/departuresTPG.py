from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

STOPS = ["Prévessin-Moëns, mairie", "Ornex, Prénepla", "Meyrin, CERN"]

def get_departures(stop_name):
    url = "https://transport.opendata.ch/v1/stationboard"
    params = {
        "station": stop_name,
        "limit": 6
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
            # Fix timezone format for Python
            if departure_time[-5] in ["+", "-"] and departure_time[-3] != ":":
                # Convert +0200 → +02:00
                departure_time = departure_time[:-2] + ":" + departure_time[-2:]

            dt = datetime.fromisoformat(departure_time)

            # Clock time
            clock_time = dt.strftime("%H:%M")

            # Countdown
            now = datetime.now(dt.tzinfo)
            minutes = int((dt - now).total_seconds() / 60)

            if minutes <= 0:
                countdown = "NOW"
            else:
                countdown = f"{minutes} min"

            # Combine both
            time_str = f"{clock_time} ({countdown})"
        else:
            time_str = "??" 
        

        delay = stop_info.get("delay", 0)
        delay_str = f"+{delay} min" if delay else "on time"

        departures.append({
            "time": time_str,
            "line": line,
            "destination": destination,
            "delay": delay_str
        })

    return departures

@app.route("/")
def index():
    all_stops = []

    for stop in STOPS:
        all_stops.append({
            "name": stop,
            "departures": get_departures(stop)
        })

    now_time = datetime.now()
    return render_template("index.html", stops=all_stops, now=now_time)

from flask import jsonify

def get_aRoute():

    params = {
        "from": "Prévessin, Prenepla",
        "to": "Genève",
        "limit": 3
    }

    URL = "https://transport.opendata.ch/v1/connections"
    
    r = requests.get(URL, params=params)
    data = r.json()

    now = datetime.now().astimezone()  # local time with timezone
    results = []

    for conn in data.get("connections", []):
        dep_str = conn["from"]["departure"]

        # Fix timezone format (+0200 -> +02:00)
        if dep_str[-5] in ['+', '-']:
            dep_str = dep_str[:-2] + ':' + dep_str[-2:]

        dep = datetime.fromisoformat(dep_str).astimezone()

        minutes = int((dep - now).total_seconds() // 60)
        if minutes < 0:
            continue

        line = (
            conn["sections"][0]["journey"]["number"]
            if conn["sections"][0].get("journey")
            else conn["products"][0]
        )

        line = line.replace("Bus ", "")
        time_str = dep.strftime("%H:%M")

        results.append({
            "text": f"{line} {time_str} {minutes}m"
        })

    return results

@app.route("/lametric")

#   def lametric():
#       data = {
#            "frames": [
#                {
#                    "text": "09:54 Lyon",
#                    "icon": 1234
#                },
#                {
#                    "text": "On time",
#                   "icon": 5678
#                }
#            ]
#        }
#        return jsonify(data)


def lametric():

    deps = get_aRoute()

    frames = []

    # ⏰ Current time + day
    now_local = datetime.now()
    frames.append({
        "text": now_local.strftime("%a %H:%M")
    })

    # 🚆 Departures with time
    for d in deps:
        frames.append(d)

    if not deps:
        frames.append({"text": "No buses"})

    return jsonify({
        "frames": frames
    })

if __name__ == "__main__":
    app.run(debug=True)
