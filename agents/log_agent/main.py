import win32evtlog
import requests
from datetime import datetime

MCP_URL = "http://127.0.0.1:8000/tool/new_incident"
API_KEY = "CHANGE_ME"

server = "localhost"
logtype = "System"
hand = win32evtlog.OpenEventLog(server, logtype)

while True:
    events = win32evtlog.ReadEventLog(
        hand,
        win32evtlog.EVENTLOG_BACKWARDS_READ |
        win32evtlog.EVENTLOG_SEQUENTIAL_READ,
        0
    )
    for ev in events:
        if ev.EventType == win32evtlog.EVENTLOG_ERROR_TYPE:
            payload = {
                "host": server,
                "source": "WindowsEventLog",
                "event_id": ev.EventID,
                "level": "ERROR",
                "message": str(ev.StringInserts),
                "timestamp": datetime.utcnow().isoformat()
            }
            requests.post(
                MCP_URL,
                json=payload,
                headers={"X-API-Key": API_KEY}
            )
# Log agent placeholder
