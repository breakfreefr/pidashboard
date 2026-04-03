from flask import Flask, render_template
from datetime import datetime, timedelta
import random

app = Flask(__name__)

DESTINATIONS = ["GENEVA", "LAUSANNE", "ZURICH", "BERN", "LYON"]

def generate_departures():
    departures = []
    now = datetime.now()

    for i in range(6):
        time = (now + timedelta(minutes=i*7)).strftime("%H:%M")
        destination = random.choice(DESTINATIONS)
        platform = str(random.randint(1, 5))

        delay = random.choice([0, 0, 0, 5])  # mostly on time
        if delay:
            status = f"DELAYED {delay} MIN"
            is_delay = True
        else:
            status = "ON TIME"
            is_delay = False

        departures.append({
            "time": time,
            "destination": destination,
            "platform": platform,
            "status": status,
            "delay": is_delay
        })

    return departures

@app.route("/")
def index():
    return render_template("Index.html", departures=generate_departures())

if __name__ == "__main__":
    app.run(debug=True)