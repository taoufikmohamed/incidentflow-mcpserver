from fastapi import FastAPI
import requests
import os

app = FastAPI()
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")

@app.post("/new")
def new_incident(data: dict):
    text = f"""
🚨 *Incident Detected*
Severity: {data['severity']}
Host: {data['host']}
Message: {data['message']}
"""
    requests.post(SLACK_WEBHOOK, json={"text": text})
    return {"status": "sent"}
# Slack agent placeholder
