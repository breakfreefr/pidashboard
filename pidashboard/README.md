# TPG → LaMetric Integration (Summary)

Display real-time TPG departures on LaMetric via a local Python service.

**Flow:** OpenTransport API → Python service → `/data` endpoint → LaMetric polls.

**Repo structure:**
```
/pidashboard/
app.py           # Python server
transport.py     # API logic (optional)
requirements.txt
/docs/tpg_lametric_integration.md
```
**Key points:**
- Python service fetches selected lines (60, 61, 64, 68) from OpenTransport.
- Adjusts timezone if needed.
- Returns JSON for LaMetric: `{"frames":[{"text":"60 12:05 | 61 12:12"}]}`.
- LaMetric polls endpoint every 30–60s.
- Common issues: 401 (auth), URL not found, incorrect time.
- Run service: `python3 app.py` or `nohup python3 app.py &`.

**Future improvements:** icons per line, countdown in minutes, multiple stops, cache API, train + bus integration.

Quick and simple: Python grabs data, LaMetric displays it—your wall now whispers departures 🚉✨.
