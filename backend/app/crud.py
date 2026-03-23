from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta

from app import models, schemas


# ── Shipments ──────────────────────────────────────────────
def get_shipments(db: Session, skip: int = 0, limit: int = 100, status: str | None = None):
    q = db.query(models.Shipment)
    if status:
        q = q.filter(models.Shipment.status == status)
    return q.order_by(models.Shipment.created_at.desc()).offset(skip).limit(limit).all()


def get_shipment(db: Session, shipment_id: int):
    return db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()


def create_shipment(db: Session, shipment: schemas.ShipmentCreate):
    db_obj = models.Shipment(**shipment.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_shipment(db: Session, shipment_id: int, updates: schemas.ShipmentUpdate):
    db_obj = db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()
    if not db_obj:
        return None
    for key, val in updates.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, val)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# ── Incidents ──────────────────────────────────────────────
def get_incidents(db: Session, skip: int = 0, limit: int = 100, status: str | None = None, severity: str | None = None):
    q = db.query(models.Incident)
    if status:
        q = q.filter(models.Incident.status == status)
    if severity:
        q = q.filter(models.Incident.severity == severity)
    return q.order_by(models.Incident.created_at.desc()).offset(skip).limit(limit).all()


def get_incident(db: Session, incident_id: int):
    return db.query(models.Incident).filter(models.Incident.id == incident_id).first()


def create_incident(db: Session, incident: schemas.IncidentCreate):
    db_obj = models.Incident(**incident.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_incident(db: Session, incident_id: int, updates: schemas.IncidentUpdate):
    db_obj = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not db_obj:
        return None
    for key, val in updates.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, val)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# ── Alerts ─────────────────────────────────────────────────
def get_alerts(db: Session, skip: int = 0, limit: int = 50, acknowledged: bool | None = None):
    q = db.query(models.Alert)
    if acknowledged is not None:
        q = q.filter(models.Alert.acknowledged == (1 if acknowledged else 0))
    return q.order_by(models.Alert.created_at.desc()).offset(skip).limit(limit).all()


def create_alert(db: Session, alert: schemas.AlertCreate):
    db_obj = models.Alert(**alert.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def acknowledge_alert(db: Session, alert_id: int):
    db_obj = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not db_obj:
        return None
    db_obj.acknowledged = 1
    db.commit()
    db.refresh(db_obj)
    return db_obj


# ── Metrics ────────────────────────────────────────────────
def get_metrics(db: Session, metric_name: str | None = None, region: str | None = None, limit: int = 200):
    q = db.query(models.OperationsMetric)
    if metric_name:
        q = q.filter(models.OperationsMetric.metric_name == metric_name)
    if region:
        q = q.filter(models.OperationsMetric.region == region)
    return q.order_by(models.OperationsMetric.recorded_at.desc()).limit(limit).all()


def create_metric(db: Session, metric: schemas.MetricCreate):
    db_obj = models.OperationsMetric(**metric.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# ── KPI Summary ───────────────────────────────────────────
def get_kpi_summary(db: Session) -> schemas.KPISummary:
    total_incidents = db.query(func.count(models.Incident.id)).scalar() or 0
    open_incidents = db.query(func.count(models.Incident.id)).filter(
        models.Incident.status.in_(["open", "investigating"])
    ).scalar() or 0
    critical_incidents = db.query(func.count(models.Incident.id)).filter(
        models.Incident.severity == "critical",
        models.Incident.status.in_(["open", "investigating"]),
    ).scalar() or 0
    active_alerts = db.query(func.count(models.Alert.id)).filter(
        models.Alert.acknowledged == 0
    ).scalar() or 0
    delayed_shipments = db.query(func.count(models.Shipment.id)).filter(
        models.Shipment.status == "delayed"
    ).scalar() or 0
    total_shipments = db.query(func.count(models.Shipment.id)).scalar() or 0

    # Average resolution time for resolved incidents (hours)
    resolved = (
        db.query(models.Incident)
        .filter(models.Incident.resolved_at.isnot(None))
        .all()
    )
    avg_hours = None
    if resolved:
        deltas = [(i.resolved_at - i.created_at).total_seconds() / 3600 for i in resolved]
        avg_hours = round(sum(deltas) / len(deltas), 1)

    # SLA compliance: % of shipments delivered on time
    sla_pct = None
    delivered = db.query(models.Shipment).filter(
        models.Shipment.actual_delivery.isnot(None)
    ).all()
    if delivered:
        on_time = sum(1 for s in delivered if s.actual_delivery <= s.expected_delivery)
        sla_pct = round(on_time / len(delivered) * 100, 1)

    return schemas.KPISummary(
        total_incidents=total_incidents,
        open_incidents=open_incidents,
        critical_incidents=critical_incidents,
        active_alerts=active_alerts,
        delayed_shipments=delayed_shipments,
        total_shipments=total_shipments,
        avg_resolution_hours=avg_hours,
        sla_compliance_pct=sla_pct,
    )


# ── Trend Data ─────────────────────────────────────────────
def get_incident_trend(db: Session, days: int = 30):
    """Incidents created per day for the last N days."""
    cutoff = datetime.utcnow() - timedelta(days=days)
    rows = (
        db.query(
            func.date(models.Incident.created_at).label("day"),
            func.count(models.Incident.id).label("count"),
        )
        .filter(models.Incident.created_at >= cutoff)
        .group_by(func.date(models.Incident.created_at))
        .order_by(func.date(models.Incident.created_at))
        .all()
    )
    return [{"date": str(r.day), "incidents": r.count} for r in rows]


def get_shipment_delay_by_region(db: Session):
    """Delayed shipment counts grouped by destination region."""
    rows = (
        db.query(
            models.Shipment.destination,
            func.count(models.Shipment.id).label("delays"),
        )
        .filter(models.Shipment.status == "delayed")
        .group_by(models.Shipment.destination)
        .all()
    )
    return [{"region": r.destination, "delays": r.delays} for r in rows]
