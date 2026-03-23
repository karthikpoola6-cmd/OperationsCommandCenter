# Architecture Overview

## System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                    Operations Command Center                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│   │  Shipment     │    │  IT Systems   │    │  Metrics     │      │
│   │  Events       │    │  Events       │    │  Feeds       │      │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│          │                    │                    │              │
│          └────────────┬───────┴────────────┬──────┘              │
│                       ▼                    ▼                     │
│          ┌─────────────────────────────────────┐                │
│          │       Anomaly Detection Engine       │                │
│          │  - Delay detection (>12hr threshold)  │                │
│          │  - SLA breach detection (>24hr)       │                │
│          │  - Metric threshold violations        │                │
│          └─────────────┬───────────────────────┘                │
│                        ▼                                        │
│          ┌─────────────────────────────────────┐                │
│          │         PostgreSQL Database          │                │
│          │  - shipments    - incidents           │                │
│          │  - alerts       - operations_metrics  │                │
│          └─────────────┬───────────────────────┘                │
│                        ▼                                        │
│          ┌─────────────────────────────────────┐                │
│          │        FastAPI Backend (REST)        │                │
│          │  - CRUD operations                   │                │
│          │  - KPI aggregation                   │                │
│          │  - Trend analytics                   │                │
│          └──────────┬──────────────────────────┘                │
│                     ▼                                           │
│     ┌───────────────────────────────────────────┐               │
│     │          React Dashboard (MUI)            │               │
│     │  - KPI Cards    - Incident Table          │               │
│     │  - Alert Panel  - Analytics Charts        │               │
│     │  - Shipment Tracker                       │               │
│     └───────────────┬───────────────────────────┘               │
│                     ▼                                           │
│     ┌───────────────────────────────────────────┐               │
│     │      AI Summarizer (Claude API)           │               │
│     │  - Root-cause analysis                    │               │
│     │  - Recommended actions                    │               │
│     │  - Preventive measures                    │               │
│     │  - Rule-based fallback when no API key    │               │
│     └───────────────────────────────────────────┘               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Model

### shipments
Tracks orders across the supply chain lifecycle.

| Column            | Type     | Description                      |
|-------------------|----------|----------------------------------|
| id                | int (PK) | Auto-increment ID                |
| order_id          | string   | Business order identifier        |
| origin            | string   | Ship-from location               |
| destination       | string   | Ship-to location                 |
| carrier           | string   | Shipping carrier                 |
| status            | enum     | pending/in_transit/delayed/delivered/failed |
| priority          | string   | normal/high/critical             |
| expected_delivery | datetime | Committed delivery date          |
| actual_delivery   | datetime | Actual delivery (null if pending)|

### incidents
Operational events requiring investigation and resolution.

| Column        | Type     | Description                         |
|---------------|----------|-------------------------------------|
| id            | int (PK) | Auto-increment ID                   |
| title         | string   | Short incident description          |
| incident_type | string   | shipment_delay/system_outage/sla_breach/data_quality |
| severity      | enum     | low/medium/high/critical            |
| status        | enum     | open/investigating/resolved/closed  |
| assigned_team | string   | Responsible operations team         |
| shipment_id   | int (FK) | Linked shipment (if applicable)     |
| ai_summary    | text     | AI-generated root-cause analysis    |

### alerts
Time-stamped notifications triggered by anomaly detection.

### operations_metrics
Time-series KPI data (on-time delivery rate, resolution time, volume, etc.)

## Key Design Patterns

1. **On-demand anomaly detection** — `/api/detect/run` scans all data and creates incidents/alerts
2. **AI with graceful degradation** — Claude API for summaries, rule-based fallback when unavailable
3. **KPI aggregation at query time** — Real-time accuracy without materialized view complexity
4. **Severity escalation** — SLA breaches auto-escalate incidents to critical
