from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# --- Shipment ---
class ShipmentBase(BaseModel):
    order_id: str
    origin: str
    destination: str
    carrier: Optional[str] = None
    status: str = "pending"
    priority: str = "normal"
    expected_delivery: datetime
    actual_delivery: Optional[datetime] = None


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(BaseModel):
    status: Optional[str] = None
    actual_delivery: Optional[datetime] = None
    carrier: Optional[str] = None


class ShipmentResponse(ShipmentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# --- Incident ---
class IncidentBase(BaseModel):
    title: str
    incident_type: str
    description: Optional[str] = None
    severity: str = "medium"
    assigned_team: Optional[str] = None
    shipment_id: Optional[int] = None


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    status: Optional[str] = None
    severity: Optional[str] = None
    assigned_team: Optional[str] = None
    root_cause: Optional[str] = None
    resolved_at: Optional[datetime] = None


class IncidentResponse(IncidentBase):
    id: int
    status: str
    root_cause: Optional[str] = None
    ai_summary: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# --- Alert ---
class AlertBase(BaseModel):
    alert_type: str
    message: str
    severity: str = "medium"
    incident_id: Optional[int] = None


class AlertCreate(AlertBase):
    pass


class AlertResponse(AlertBase):
    id: int
    acknowledged: int
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Metrics ---
class MetricBase(BaseModel):
    metric_name: str
    metric_value: float
    unit: str = "count"
    region: Optional[str] = None


class MetricCreate(MetricBase):
    pass


class MetricResponse(MetricBase):
    id: int
    recorded_at: datetime

    model_config = {"from_attributes": True}


# --- Dashboard KPIs ---
class KPISummary(BaseModel):
    total_incidents: int
    open_incidents: int
    critical_incidents: int
    active_alerts: int
    delayed_shipments: int
    total_shipments: int
    avg_resolution_hours: Optional[float] = None
    sla_compliance_pct: Optional[float] = None
