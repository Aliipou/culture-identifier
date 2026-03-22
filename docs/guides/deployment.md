# Deployment Guide

```bash
docker compose up --build -d
curl -X POST http://localhost:8000/identify -H 'Content-Type: application/json' -d '{"text": "Hyvaa huomenta!"}'
```

Kubernetes: 3 replicas, 2GB RAM, readiness probe at `/health/ready`.
