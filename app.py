from fastapi import FastAPI, Request
from decision_engine import decide_action
from remediation.runner import run_action
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Auto-Remediation API is Online",
        "status": "Healthy",
        "docs": "/docs"
    }

@app.post("/alert")
async def receive_alert(request: Request):
    data = await request.json()
    
    
    alerts = data.get('alerts', [])
    if not alerts:
        return {"status": "error", "message": "No alerts found in payload"}

    
    labels = alerts[0].get('labels', {})
    alert_name = labels.get('alertname', 'UnknownAlert')
    instance = labels.get('instance', 'unknown-host')

    print(f"[ALERT RECEIVED] {alert_name} on {instance}")

    
    action = decide_action(alert_name)
    result = run_action(action, instance)

    return {"status": "processed", "action": action, "result": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
