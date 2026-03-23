from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Enum
from sqlalchemy.sql import func
import enum

from app.database import Base


class SeverityLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class IncidentStatus(str, enum.Enum):
    open = "open"
    investigating = "investigating"
    resolved = "resolved"
    closed = "closed"


class ShipmentStatus(str, enum.Enum):
    pending = "pending"
    in_transit = "in_transit"
    delayed = "delayed"
    delivered = "delivered"
    failed = "failed"


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(50), unique=True, nullable=False)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    carrier = Column(String(100))
    status = Column(String(20), default=ShipmentStatus.pending)
    priority = Column(String(10), default="normal")
    expected_delivery = Column(DateTime, nullable=False)
    actual_delivery = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    incident_type = Column(String(50), nullable=False)
    description = Column(Text)
    severity = Column(String(20), default=SeverityLevel.medium)
    status = Column(String(20), default=IncidentStatus.open)
    assigned_team = Column(String(100))
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=True)
    root_cause = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    resolved_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), default=SeverityLevel.medium)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)
    acknowledged = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())


class OperationsMetric(Base):
    __tablename__ = "operations_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    unit = Column(String(30), default="count")
    region = Column(String(50))
    recorded_at = Column(DateTime, server_default=func.now())
