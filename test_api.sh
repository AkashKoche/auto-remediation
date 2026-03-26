#!/bin/bash
ENDPOINT="http://192.168.59.100:30007/alert"

echo "--- Testing Remediation API Flow ---"

echo "Triggering CPU Restart..."
curl -s -X POST "$ENDPOINT" \
     -H "Content-Type: application/json" \
     -d '{"alerts": [{"labels": {"alertname": "HighCPUUsage", "instance": "prod-app-01"}}]}' | python -m json.tool

echo -e "\nTriggering Disk Cleanup..."
curl -s -X POST "$ENDPOINT" \
     -H "Content-Type: application/json" \
     -d '{"alerts": [{"labels": {"alertname": "DiskFull", "instance": "prod-db-01"}}]}' | python3 -m json.tool
