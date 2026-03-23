from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


@router.get("/", response_model=list[schemas.AlertResponse])
def list_alerts(
    skip: int = 0,
    limit: int = 50,
    acknowledged: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    return crud.get_alerts(db, skip=skip, limit=limit, acknowledged=acknowledged)


@router.post("/", response_model=schemas.AlertResponse, status_code=201)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    return crud.create_alert(db, alert)


@router.patch("/{alert_id}/acknowledge", response_model=schemas.AlertResponse)
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = crud.acknowledge_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert
