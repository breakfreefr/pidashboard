import requests
from datetime import datetime, timezone

# ---- CONFIG ----
LAMETRIC_IP = "192.168.1.146"
API_KEY = "4a8c3fc44adb1ad57394e60d8ade56e85b6446da6be70717700acd37d18e91b5"

URL = "https://transport.opendata.ch/v1/connections"

LAMETRIC_URL = f"http://{LAMETRIC_IP}:8080/api/v2/device/apps/com.lametric.32e04f0f3d2f2c9eaa0d2d1f1f/data"

# ---- HELPERS ----
def parse_time(dt_str):
    return datetime.fromisoformat(dt_str)

def fetch_departures():
    params = {
        "from": "Prévessin, Prenepla",
        "to": "Genève",
        "limit": 3
    }

    r = requests.get(URL, params=params)
    data = r.json()

    now = datetime.now(timezone.utc)
    results = []

    for conn in data.get("connections", []):
        dep_str = conn["from"]["departure"]
        dep = parse_time(dep_str).astimezone(timezone.utc)

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

# ---- FORMAT FOR LAMETRIC ----
def build_payload(deps):
    frames = []

    for d in deps:
        frames.append({
            "text": f"{d['line']} {d['minutes']}m"
        })

    if not frames:
        frames.append({"text": "No trains"})

    return {"frames": frames}

# ---- PUSH TO LAMETRIC ----
def send_to_lametric(payload):
    headers = {
        "X-Access-Token": API_KEY
    }

    r = requests.put(LAMETRIC_URL, json=payload, headers=headers)
    print("Status:", r.status_code)

# ---- MAIN ----
if __name__ == "__main__":
    deps = fetch_departures()
    payload = build_payload(deps)
    send_to_lametric(payload)