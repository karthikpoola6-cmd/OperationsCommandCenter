from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])


@router.get("/", response_model=list[schemas.IncidentResponse])
def list_incidents(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_incidents(db, skip=skip, limit=limit, status=status, severity=severity)


@router.get("/trend")
def incident_trend(days: int = 30, db: Session = Depends(get_db)):
    return crud.get_incident_trend(db, days=days)


@router.get("/{incident_id}", response_model=schemas.IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    inc = crud.get_incident(db, incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return inc


@router.post("/", response_model=schemas.IncidentResponse, status_code=201)
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(get_db)):
    return crud.create_incident(db, incident)


@router.patch("/{incident_id}", response_model=schemas.IncidentResponse)
def update_incident(
    incident_id: int,
    updates: schemas.IncidentUpdate,
    db: Session = Depends(get_db),
):
    inc = crud.update_incident(db, incident_id, updates)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return inc
