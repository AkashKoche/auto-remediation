from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import os
import uvicorn

# Internal modules
from decision_engine import decide_action
from remediation.runner import run_action

app = FastAPI()

# --- CONFIGURATION ---
# In production, this would come from a K8s Secret
API_KEY = os.getenv("REMEDIATION_TOKEN", "secret-key-123")

# --- PROMETHEUS METRICS ---
REMEDIATION_COUNT = Counter(
    'remediation_triggered_total', 
    'Total number of auto-remediations triggered',
    ['alert_name', 'instance', 'action']
)

EXECUTION_TIME = Histogram(
    'remediation_duration_seconds', 
    'Time spent executing remediation scripts',
    ['action']
)

# --- ROUTES ---

@app.get("/")
def read_root():
    return {
        "message": "Auto-Remediation API is Online",
        "status": "Healthy",
        "docs": "/docs"
    }

@app.get("/metrics")
def metrics():
    """Endpoint for Prometheus scraping"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/alert")
async def receive_alert(request: Request, x_auth_token: str = Header(None)):
    # 1. Security Check
    if x_auth_token != API_KEY:
        print(f"[SECURITY] Unauthorized access attempt blocked.")
        raise HTTPException(status_code=403, detail="Invalid or missing Auth Token")

    # 2. Parse Payload
    data = await request.json()
    alerts = data.get('alerts', [])
    
    if not alerts:
        return {"status": "error", "message": "No alerts found in payload"}

    # 3. Extract metadata
    labels = alerts[0].get('labels', {})
    alert_name = labels.get('alertname', 'UnknownAlert')
    instance = labels.get('instance', 'unknown-host')

    print(f"[AUTH SUCCESS] Processing {alert_name} for {instance}")

    # 4. Decision & Execution with Metrics Tracking
    action = decide_action(alert_name)
    
    start_time = time.time()
    result = run_action(action, instance)
    duration = time.time() - start_time
    
    # 5. Update Prometheus
    REMEDIATION_COUNT.labels(alert_name=alert_name, instance=instance, action=action).inc()
    EXECUTION_TIME.labels(action=action).observe(duration)

    return {
        "status": "processed", 
        "action": action, 
        "result": result,
        "duration_seconds": round(duration, 4)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
