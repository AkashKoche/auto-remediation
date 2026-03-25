#BUILD and RUN

    docker build -t auto-remediation:v1 .

    docker run -p 8000:8000 auto-remediation:v1

#TEST

    curl http://localhost:8000/docs

#DEPLOY

    kubectl apply -f deployment.yaml

    kubectl apply -f service.yaml

#CHECK

    kubectl get pods

    kubectl get svc

#EXPOSE API

    kubectl get nodes -o wide

    http://<NODE-IP>:30007/alert

#CONFIGURE ALERTMANAGER WEBHOOK

receivers:
  - name: "auto-remediation"
    webhook_configs:
      - url: "http://<NODE-IP>:30007/alert"

#TEST END-TO-END

curl -X POST http://<NODE-IP>:30007/alert \
-H "Content-Type: application/json" \
-d '{
  "alerts": [
    {
      "labels": {
        "alertname": "HighCPUUsage",
        "instance": "pod-1"
      }
    }
  ]
}'

#APPLY LIVENESS & READINESS PROBES

    kubectl patch deployment auto-remediation --patch-file liveness-patch.yaml

    kubectl patch deployment auto-remediation --patch-file readiness-patch.yaml

#HORIZONTAL POD AUTOSCALER (HPA)

    kubectl autoscale deployment auto-remediation \
    --cpu-percent=50 --min=2 --max=5

#INGRESS (OPTIONAL)

    kubectl apply -f ingress.yaml
