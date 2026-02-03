# MCP server placeholder
from fastapi import FastAPI, Depends, Header, HTTPException
from shared.incident_schema import Incident
from mcp_server.severity_ai import classify_severity
import requests
import os
print("API KEY =", os.getenv("INCIDENTFLOW_API_KEY"), flush=True)

app = FastAPI()
API_KEY = os.getenv("INCIDENTFLOW_API_KEY")
SLACK_AGENT_URL = "http://127.0.0.1:9001/incident"

def auth(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/tool/new_incident", dependencies=[Depends(auth)])
def new_incident(incident: Incident):
    incident.severity = classify_severity(incident)
    requests.post(SLACK_AGENT_URL, json=incident.model_dump(mode='json'))
    return {"status": "accepted", "severity": incident.severity}
