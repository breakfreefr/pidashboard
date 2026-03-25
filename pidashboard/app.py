from flask import Flask, jsonify, render_template
from datetime import datetime
import requests

app = Flask(__name__)

URL = "https://transport.opendata.ch/v1/connections"

def parse_time(dt_str):
    return datetime.fromisoformat(dt_str)


def get_departures():
    params = {
        "from": "Prévessin, Prenepla",
        "to": "Genève",
        "limit": 3
    }

    r = requests.get(URL, params=params)
    data = r.json()

    now = datetime.now().astimezone()  # local time with timezone
    results = []

    for conn in data.get("connections", []):
        dep_str = conn["from"]["departure"]

        # Parse ISO time (already includes timezone if provided)
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
                "line": line,
                "time": time_str,
                "minutes": minutes

        })

    return results




@app.route("/data")
def data():
    now = datetime.now().strftime("%H:%M")

    return jsonify({
        "time": now,
        "weather": "12°C Cloudy",  # replace later with real API
        "departures": get_departures()
    })




@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
