import requests
import json

URL = "http://192.168.59.100:30007/alert"

def trigger_test(alert_name, target_instance):
    payload = {
        "alerts": [
            {
                "labels": {
                    "alertname": alert_name,
                    "instance": target_instance
                }
            }
        ]
    }
    print(f"Testing: {alert_name} on {target_instance}")

    headers = {
            "X-Auth-Token": "secret-key-123",
            "Content-Type": "application/json"
    }

    response = requests.post(URL, json=payload, headers=headers)

    print(f"Status Code: {response.status_code}")
    print(f"Raw Content: '{response.text}'")

    if response.text.strip():
        print(json.dumps(response.json(), indent=2))
    else:
        print("Error: Received an empty response from the server.")

if __name__ == "__main__":
    trigger_test("HighCPUUsage", "web-server-01")
    trigger_test("DiskFull", "db-node-01")
