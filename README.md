# Akelo Dashboard (React + FastAPI) — Combined Docker Build

This package contains a full-stack app that serves a React frontend from a FastAPI backend.
The Excel file `AKELO_FAMILY_ASSOCIATION_2024.xlsx` is embedded in `backend/data/`.

## Quick run (Docker)
```bash
docker-compose up --build
```
Frontend: http://localhost:3000
Backend API: http://localhost:8000/api

## Deploy to Render
A `render.yaml` is included for a single combined service. You can upload this repo to Render and set service name `akelo-dashboard`.
