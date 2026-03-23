# Architecture

## How It Works

```
┌──────────────────────────────────────────────────┐
│            Operations Command Center              │
│                                                    │
│   Shipment Events    IT Events    Metric Feeds    │
│         │               │              │          │
│         └───────┬───────┴──────┬───────┘          │
│                 ▼              ▼                   │
│        Anomaly Detection Engine                   │
│        - Delay detection (>12hr)                  │
│        - SLA breach detection (>24hr)             │
│                 ▼                                  │
│           PostgreSQL                              │
│        - shipments                                │
│        - incidents                                │
│        - alerts                                   │
│        - operations_metrics                       │
│                 ▼                                  │
│         FastAPI Backend                           │
│        - REST API                                 │
│        - KPI aggregation                          │
│                 ▼                                  │
│     React Dashboard    Power BI Dashboards        │
│                 ▼                                  │
│       AI Summarizer (Claude API)                  │
│       - Root-cause analysis                       │
│       - Recommended actions                       │
│       - Rule-based fallback                       │
└──────────────────────────────────────────────────┘
```

## Data Model

**shipments** — Tracks orders from origin to destination with carrier, status, priority, and delivery dates.

**incidents** — Operational events needing investigation. Linked to shipments when applicable. Tracks severity, status, assigned team, and AI-generated summaries.

**alerts** — Notifications triggered by anomaly detection. Linked to incidents. Can be acknowledged by operators.

**operations_metrics** — Time-series KPI data: on-time delivery rate, average resolution time, shipment volume by region.
