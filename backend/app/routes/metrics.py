from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/api/metrics", tags=["Metrics"])


@router.get("/", response_model=list[schemas.MetricResponse])
def list_metrics(
    metric_name: Optional[str] = None,
    region: Optional[str] = None,
    limit: int = 200,
    db: Session = Depends(get_db),
):
    return crud.get_metrics(db, metric_name=metric_name, region=region, limit=limit)


@router.post("/", response_model=schemas.MetricResponse, status_code=201)
def create_metric(metric: schemas.MetricCreate, db: Session = Depends(get_db)):
    return crud.create_metric(db, metric)


@router.get("/kpi", response_model=schemas.KPISummary)
def kpi_summary(db: Session = Depends(get_db)):
    return crud.get_kpi_summary(db)


@router.get("/delays-by-region")
def delays_by_region(db: Session = Depends(get_db)):
    return crud.get_shipment_delay_by_region(db)
