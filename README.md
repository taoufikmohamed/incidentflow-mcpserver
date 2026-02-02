# IncidentFlow

Incident automation platform.

IncidentFlow automatically detects Windows system errors, classifies severity using AI, and creates Slack incidents — all running as Windows services.

# IncidentFlow

IncidentFlow is a Windows-based incident automation platform that detects system errors, classifies severity using AI, and creates Slack incidents.

## Features
- Windows Event Log monitoring
- AI severity classification
- Slack incident creation
- Runs as Windows services (NSSM)

## Install
1. Install Python 3.11
2. Install NSSM
3. Clone repo
4. Configure environment variables
5. Run `install\nssm-install.ps1`

## Commands
python -m uvicorn agents.slack_agent.main:app --host 127.0.0.1 --port 9001 (OR)
python -m uvicorn agents.slack_agent.main:app --port 9001

python -c "import agents.slack_agent.main; print('OK')"

MCP Server (FastAPI + uvicorn)  
   nssm install IncidentFlow-MCP

    Application tab

        Path
        
        C:\python.exe
        
        
        Arguments
        
        -m uvicorn mcp_server.server:app --host 127.0.0.1 --port 8000
        
        
        Startup directory
        
        C:\incidentflow-mcpserver

IncidentFlow-Slack
   nssm install IncidentFlow-Slack
    Application tab
        Path
        
        C:\Python311\python.exe
        Arguments
        
        -m uvicorn agents.slack_agent.main:app --host 127.0.0.1 --port 9001
        Startup directory
        
        C:\incidentflow-mcpserver

IncidentFlow-LogAgent
   nssm install IncidentFlow-LogAgent
    Application tab
        Path
        
        C:\Python311\python.exe
        Arguments
        
        agents\log_agent\main.py
        Startup directory
        
        C:\incidentflow-mcpserver

Powershell
    Set environment variables (securely)

    nssm set IncidentFlow-MCP AppEnvironmentExtra `
    "INCIDENTFLOW_API_KEY=supersecretkey"
    nssm set IncidentFlow-MCP AppEnvironmentExtra `
    "DEESEEK_API_KEY=your_deepseek_key"
    nssm set IncidentFlow-Slack AppEnvironmentExtra `
    "SLACK_WEBHOOK_URL=https://hooks.slack.com/..."

    
    START SERVICES (IN CORRECT ORDER)

        nssm start IncidentFlow-Slack
        nssm start IncidentFlow-MCP
        nssm start IncidentFlow-LogAgent

        nssm status IncidentFlow-MCP
    
 
    Test MCP API manually (PowerShell-safe)

         Invoke-RestMethod `
              -Uri http://127.0.0.1:8000/tool/new_incident `
              -Method POST `
              -Headers @{ "X-API-Key" = "supersecretkey" } `
              -Body (@{
                host = "TEST-HOST"
                source = "ManualTest"
                event_id = 9999
                level = "ERROR"
                message = "Disk failure detected"
                timestamp = (Get-Date).ToString("o")
              } | ConvertTo-Json) `
              -ContentType "application/json"

    Expected response
        {
          "status": "ok",
          "severity": "CRITICAL"
        }
    Verify Slack message

         expected message
                 Incident Detected
                    Severity: CRITICAL
                    Host: TEST-HOST
                    Message: Disk failure detected
