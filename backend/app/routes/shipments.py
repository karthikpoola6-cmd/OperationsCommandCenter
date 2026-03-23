from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/api/shipments", tags=["Shipments"])


@router.get("/", response_model=list[schemas.ShipmentResponse])
def list_shipments(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_shipments(db, skip=skip, limit=limit, status=status)


@router.get("/{shipment_id}", response_model=schemas.ShipmentResponse)
def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    ship = crud.get_shipment(db, shipment_id)
    if not ship:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return ship


@router.post("/", response_model=schemas.ShipmentResponse, status_code=201)
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    return crud.create_shipment(db, shipment)


@router.patch("/{shipment_id}", response_model=schemas.ShipmentResponse)
def update_shipment(
    shipment_id: int,
    updates: schemas.ShipmentUpdate,
    db: Session = Depends(get_db),
):
    ship = crud.update_shipment(db, shipment_id, updates)
    if not ship:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return ship
