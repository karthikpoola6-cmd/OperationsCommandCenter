from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.anomaly_detector import run_all_detections
from app.services.ai_summarizer import generate_incident_summary
from app import crud, schemas

router = APIRouter(prefix="/api/detect", tags=["Anomaly Detection"])


@router.post("/run")
def run_detection(db: Session = Depends(get_db)):
    """Trigger anomaly detection scan across all operational data."""
    return run_all_detections(db)


@router.post("/incidents/{incident_id}/ai-summary")
async def generate_ai_summary(incident_id: int, db: Session = Depends(get_db)):
    """Generate AI-powered root-cause summary for an incident."""
    incident = crud.get_incident(db, incident_id)
    if not incident:
        return {"error": "Incident not found"}

    summary = await generate_incident_summary(
        title=incident.title,
        incident_type=incident.incident_type,
        description=incident.description or "",
        severity=incident.severity,
    )

    # Save to incident
    crud.update_incident(
        db,
        incident_id,
        schemas.IncidentUpdate(root_cause=summary),
    )
    # Also store as ai_summary directly
    inc = crud.get_incident(db, incident_id)
    inc.ai_summary = summary
    db.commit()

    return {"incident_id": incident_id, "ai_summary": summary}
