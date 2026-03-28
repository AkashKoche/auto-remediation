import requests
import time

# Configuration
BASE_URL = "http://localhost:8000"
TOKEN = "secret-key-123"
HEADERS = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

def test_auto_remediation():
    print("🚀 Starting End-to-End Test...")

    # 1. Test Authentication (Should fail without token)
    print("\n[Step 1] Testing Security...")
    fail_res = requests.post(f"{BASE_URL}/alert", json={})
    if fail_res.status_code == 403:
        print("✅ Security Check Passed: Unauthorized request blocked.")
    else:
        print("❌ Security Check Failed!")

    # 2. Trigger a Remediation
    print("\n[Step 2] Triggering 'HighCPUUsage' Alert...")
    payload = {
        "alerts": [{
            "labels": {
                "alertname": "HighCPUUsage",
                "instance": "prod-server-01"
            }
        }]
    }
    start = time.time()
    res = requests.post(f"{BASE_URL}/alert", json=payload, headers=HEADERS)
    
    if res.status_code == 200:
        data = res.json()
        print(f"✅ Alert Processed! Action: {data['action']}, Result: {data['result']}")
    else:
        print(f"❌ Alert Failed: {res.text}")

    # 3. Verify Prometheus Metrics
    print("\n[Step 3] Verifying Observability (Metrics)...")
    metrics_res = requests.get(f"{BASE_URL}/metrics")
    if "remediation_triggered_total" in metrics_res.text:
        print("✅ Metrics Verified: 'remediation_triggered_total' found in /metrics")
    else:
        print("❌ Metrics Missing!")

if __name__ == "__main__":
    test_auto_remediation()
