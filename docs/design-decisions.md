# Design Decisions

## 1. FastAPI over Express/Node

**Decision:** Python FastAPI for the backend.

**Why:** Native data processing capabilities with pandas-ready ecosystem, automatic OpenAPI documentation, and async support. Python aligns with data engineering and analytics workflows that are core to operations monitoring.

## 2. Dark Theme Operations UI

**Decision:** Dark theme MUI dashboard.

**Why:** Real operations centers and NOCs (Network Operations Centers) universally use dark interfaces. Reduces eye strain during extended monitoring shifts and improves visual contrast for alerts and severity indicators.

## 3. AI Summarizer with Rule-Based Fallback

**Decision:** Claude API for intelligent summaries, with comprehensive rule-based fallback.

**Why:** The system must remain fully functional without external API dependencies. The fallback generates structured root-cause analysis, recommended actions, and preventive measures based on incident type — useful enough for demonstrations and environments without API access.

## 4. On-Demand Anomaly Detection

**Decision:** Detection runs via API call rather than continuous streaming.

**Why:** Simplifies the architecture while demonstrating the full detection → incident → alert pipeline. In production, this would be replaced with scheduled cron jobs or event-driven triggers (Kafka consumers).

## 5. KPI Aggregation at Query Time

**Decision:** KPIs computed from live data on each request rather than materialized views.

**Why:** Ensures real-time accuracy with the current data volume. At scale, this would be replaced with pre-computed metrics tables refreshed on schedule.

## 6. Seed Data with Realistic Scenarios

**Decision:** Pre-populated database with multi-region supply chain data, active incidents, and historical metrics.

**Why:** Enables immediate demonstration of all features without manual data entry. The seed data covers edge cases: on-time deliveries, delays, system outages, SLA breaches, and data quality issues.
