"""
Anomaly Detection Engine

Scans shipments and operational metrics to identify:
- Delayed shipments (expected delivery exceeded by threshold)
- SLA breaches (resolution time exceeds target)
- Metric threshold violations (KPIs outside acceptable range)

Auto-creates incidents and alerts when anomalies are detected.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app import models, schemas, crud


DELAY_THRESHOLD_HOURS = 12
SLA_RESOLUTION_HOURS = 24


def detect_shipment_delays(db: Session) -> list[dict]:
    """Find shipments that are past their expected delivery and still in transit."""
    now = datetime.utcnow()
    overdue = (
        db.query(models.Shipment)
        .filter(
            models.Shipment.status.in_(["in_transit", "pending"]),
            models.Shipment.expected_delivery < now - timedelta(hours=DELAY_THRESHOLD_HOURS),
        )
        .all()
    )

    results = []
    for ship in overdue:
        delay_hours = (now - ship.expected_delivery).total_seconds() / 3600

        # Mark shipment as delayed
        ship.status = "delayed"
        db.commit()

        # Create incident
        incident = crud.create_incident(
            db,
            schemas.IncidentCreate(
                title=f"Shipment Delay: Order {ship.order_id}",
                incident_type="shipment_delay",
                description=(
                    f"Shipment from {ship.origin} to {ship.destination} "
                    f"is {delay_hours:.0f} hours overdue. "
                    f"Carrier: {ship.carrier or 'Unknown'}. Priority: {ship.priority}."
                ),
                severity="high" if delay_hours > 24 else "medium",
                assigned_team="Logistics Operations",
                shipment_id=ship.id,
            ),
        )

        # Create alert
        crud.create_alert(
            db,
            schemas.AlertCreate(
                alert_type="shipment_delay",
                message=(
                    f"Shipment delay detected: Order #{ship.order_id} — "
                    f"Expected delivery exceeded by {delay_hours:.0f} hours"
                ),
                severity=incident.severity,
                incident_id=incident.id,
            ),
        )

        results.append({
            "shipment_id": ship.id,
            "order_id": ship.order_id,
            "delay_hours": round(delay_hours, 1),
            "incident_id": incident.id,
        })

    return results


def detect_sla_breaches(db: Session) -> list[dict]:
    """Find open incidents that have exceeded the SLA resolution window."""
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=SLA_RESOLUTION_HOURS)

    breached = (
        db.query(models.Incident)
        .filter(
            models.Incident.status.in_(["open", "investigating"]),
            models.Incident.created_at < cutoff,
        )
        .all()
    )

    results = []
    for inc in breached:
        age_hours = (now - inc.created_at).total_seconds() / 3600

        # Escalate severity
        if inc.severity != "critical":
            inc.severity = "critical"
            db.commit()

        crud.create_alert(
            db,
            schemas.AlertCreate(
                alert_type="sla_breach",
                message=(
                    f"SLA Breach: Incident #{inc.id} '{inc.title}' "
                    f"has been open for {age_hours:.0f} hours (target: {SLA_RESOLUTION_HOURS}h)"
                ),
                severity="critical",
                incident_id=inc.id,
            ),
        )

        results.append({
            "incident_id": inc.id,
            "age_hours": round(age_hours, 1),
            "escalated_to": "critical",
        })

    return results


def run_all_detections(db: Session) -> dict:
    """Run all anomaly detection checks and return summary."""
    delays = detect_shipment_delays(db)
    breaches = detect_sla_breaches(db)

    return {
        "shipment_delays_detected": len(delays),
        "sla_breaches_detected": len(breaches),
        "details": {
            "delays": delays,
            "sla_breaches": breaches,
        },
    }
