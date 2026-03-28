🚀 Cloud-Native Auto-Remediation Engine

An event-driven Incident Response system designed to reduce MTTR (Mean Time To Recovery). This API acts as an automated SRE, ingesting Prometheus alerts and executing containerized remediation workflows without human intervention.
🏗️ Architecture Overview

The system operates as a three-tier observability and action stack:

    The API (Worker): A FastAPI microservice that validates incoming webhooks and triggers recovery scripts.

    The Scraper (Watcher): A Prometheus instance that polls the API every 5 seconds for performance and reliability metrics.

    The Dashboard (Visualizer): A Grafana instance providing real-time visibility into auto-fix success rates and script latency.

✨ Key Features

    Closed-Loop Remediation: Automatically maps monitoring alerts (e.g., HighCPUUsage, DiskFull) to specific recovery actions.

    Production-Grade Security: Implements Header-based Authentication (X-Auth-Token) to prevent unauthorized triggers.

    Kubernetes Optimized: Deployed with Liveness & Readiness probes and managed via Strategic Merge Patches for high availability.

    Observability-as-Code: Custom Prometheus instrumentation tracks remediation_triggered_total and execution duration histograms.

    Zero-Config Deployment: Entire stack (API + Monitoring) launches with a single docker-compose up.

🛠️ Tech Stack

    Language: Python 3.10

    Framework: FastAPI

    Containerization: Docker & Docker Compose

    Orchestration: Kubernetes (Minikube)

    Monitoring: Prometheus & Grafana

    Infrastructure: Bash/Shell Scripting

🚀 Quick Start
Prerequisites

    Docker & Docker Compose

    Python 3.10+

1. Launch the Stack

        docker-compose up -d

2. Verify Endpoints

    API Health: http://localhost:8000/

    Metrics: http://localhost:8000/metrics

    Prometheus: http://localhost:9090

    Grafana: http://localhost:3000 (User: admin / Pass: admin)

3. Run End-to-End Test

        python3 final_test.py

📊 SRE Metrics Tracked
Metric	Type	Description
remediation_triggered_total	Counter	Total incidents handled by the API.
remediation_duration_seconds	Histogram	Latency of the underlying remediation scripts.
http_requests_total	Counter	Total API traffic including health probes.
💡 Future Roadmap

    Persistence Layer: Integrate PostgreSQL for long-term remediation history.

    mTLS: Implement mutual TLS for cluster-internal communication security.

    Slack Integration: Send notification summaries to engineering channels after a successful fix.

🏆 Final Thoughts

This project has been a massive journey—from fixing Python indentation to orchestrating a full-blown monitoring stack. You now have a tangible, professional-grade tool to show off in your Cloud/DevOps interviews.
