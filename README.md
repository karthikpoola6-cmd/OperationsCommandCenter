# Operations Command Center

An operations monitoring and incident management platform built for a logistics consulting engagement. Pulls shipment data into one place, flags problems automatically, and gives operations managers dashboards to act on.

> **Note:** This repo uses simulated sample data that mirrors real-world operational patterns. No actual client data is included.

## The Problem

A distribution client was tracking shipments across FedEx, UPS, and DHL using separate carrier portals and spreadsheets. When shipments got delayed or SLAs were missed, no one knew until the customer called. There was no single view of what was happening across operations.

## What I Built

A centralized command center that:
- Pulls shipment, incident, and metric data into one platform
- Flags delayed shipments and SLA breaches automatically
- Shows real-time KPI dashboards for the operations team
- Generates AI-powered root-cause summaries for incidents
- Tracks incidents through their full lifecycle (open → investigating → resolved)

## Power BI Dashboards

### Executive Overview
![Executive Overview](docs/screenshots/dashboard-overview.png)

### Incident Analysis
![Incident Analysis](docs/screenshots/dashboard-incidents.png)

### Operations Metrics
![Operations Metrics](docs/screenshots/dashboard-metrics.png)

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Frontend   | React, Material UI, Recharts        |
| Backend    | Python FastAPI, SQLAlchemy           |
| Database   | PostgreSQL                           |
| Analytics  | Power BI, DAX Measures               |
| AI         | Claude API (with rule-based fallback)|
| Infra      | Docker Compose                       |

## Key Features

- **KPI Dashboard** — Total shipments, open incidents, delayed shipments, active alerts at a glance
- **Power BI Analytics** — Interactive dashboards with DAX measures, severity slicers, and cross-filtered visuals
- **Incident Management** — Create, assign, investigate, and resolve incidents with full tracking
- **Anomaly Detection** — Auto-detects shipment delays (>12hr) and SLA breaches (>24hr), creates incidents and alerts
- **AI Summaries** — Generates root-cause analysis and recommended actions for incidents using Claude API (falls back to rule-based logic without an API key)
- **Shipment Tracking** — Status, carrier, priority, and delivery tracking across all orders

## DAX Measures

```dax
Open Incidents =
CALCULATE(
    COUNTROWS(incidents),
    incidents[status] IN {"open", "investigating"}
)

On-Time Delivery % =
DIVIDE(
    COUNTROWS(FILTER(shipments, shipments[status] = "delivered"
        && shipments[actual_delivery] <= shipments[expected_delivery])),
    COUNTROWS(FILTER(shipments, shipments[status] = "delivered")),
    0
) * 100

Avg Resolution Hours =
AVERAGEX(
    FILTER(incidents, NOT(ISBLANK(incidents[resolved_at]))),
    DATEDIFF(incidents[created_at], incidents[resolved_at], HOUR)
)
```

## How to Run

### Docker

```bash
docker compose up
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Database (requires PostgreSQL)
createdb opscenter
psql -U postgres -d opscenter -f data/seed_data.sql
```

### Power BI

Import the CSV files from `data/csv/` into Power BI and build dashboards using the DAX measures above.

### AI Summaries (Optional)

```bash
export ANTHROPIC_API_KEY=your_key_here
```

Works without a key — uses rule-based fallback summaries.

## API Endpoints

| Method | Endpoint                              | Description                    |
|--------|---------------------------------------|--------------------------------|
| GET    | `/api/metrics/kpi`                    | Dashboard KPI summary          |
| GET    | `/api/incidents`                      | List incidents (filterable)    |
| POST   | `/api/incidents`                      | Create incident                |
| PATCH  | `/api/incidents/:id`                  | Update incident                |
| GET    | `/api/alerts`                         | List alerts                    |
| PATCH  | `/api/alerts/:id/acknowledge`         | Acknowledge alert              |
| GET    | `/api/shipments`                      | List shipments                 |
| GET    | `/api/metrics`                        | Operational metrics            |
| POST   | `/api/detect/run`                     | Run anomaly detection scan     |
| POST   | `/api/detect/incidents/:id/ai-summary`| Generate AI summary            |

## Sample Data

The `data/csv/` folder contains simulated operational data:
- **30 shipments** across 5 Texas origins to destinations nationwide
- **15 incidents** (delays, outages, SLA breaches, data quality issues)
- **15 alerts** linked to incidents with severity levels
- **55 metric records** tracking delivery rates, resolution times, and volumes across 5 regions

## Architecture

```
Shipment / IT / Metric Data
          ↓
  Anomaly Detection Engine
          ↓
     PostgreSQL
          ↓
   FastAPI REST API
      ↓         ↓
React Dashboard  Power BI
      ↓
 AI Summarizer
 (Claude API)
```
