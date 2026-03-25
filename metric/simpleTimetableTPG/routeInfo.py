import requests
from datetime import datetime

# ---- CONFIG ----
LAMETRIC_IP = "192.168.1.50"
API_KEY = "your_api_key_here"

# Station names (Swiss API format works fine here)
FROM_STATION = "Ornex, Mairie"   # try also "Prévessin, Mairie"
TO_STATION = "Genève"

LAMETRIC_URL = f"http://{LAMETRIC_IP}:8080/api/v2/device/apps/com.lametric.32e04f0f3d2f2c9eaa0d2d1f1f/data"

# ---- FETCH DATA ----
def get_departures():
    url = "https://transport.opendata.ch/v1/connections"
    params = {
        "from": FROM_STATION,
        "to": TO_STATION,
        "limit": 3
    }

    r = requests.get(url, params=params)
    data = r.json()

    results = []
    now = datetime.now()

    for conn in data.get("connections", []):
        dep_time_str = conn["from"]["departure"]
        dep_time = datetime.fromisoformat(dep_time_str.replace("Z", "+00:00"))

        minutes = int((dep_time - now).total_seconds() / 60)
        if minutes < 0:
            continue

        time_str = dep_time.strftime("%H:%M")

        results.append({
            "minutes": minutes,
            "time": time_str
        })

    return results[:3]

# ---- FORMAT FOR LAMETRIC ----
def build_frames(departures):
    frames = []

    for dep in departures:
        frames.append({
            "text": f"GEN {dep['minutes']}m"
        })

    if not frames:
        frames.append({"text": "No trains 😴"})

    return {"frames": frames}

# ---- SEND TO DEVICE ----
def send_to_lametric(payload):
    headers = {
        "X-Access-Token": API_KEY
    }

    r = requests.put(LAMETRIC_URL, json=payload, headers=headers)
    print("Status:", r.status_code)

# ---- MAIN ----
if __name__ == "__main__":
    deps = get_departures()
    payload = build_frames(deps)
    send_to_lametric(payload)