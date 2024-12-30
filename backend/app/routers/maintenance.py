from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.maintenance import Maintenance
from app.models.garage import Garage
from app.schemas.maintenance import MaintenanceCreate, MaintenanceResponse

router = APIRouter()

@router.get("/", response_model=list[MaintenanceResponse])
def get_all_maintenances(db: Session = Depends(get_db)):
    return db.query(Maintenance).all()

@router.post("/", response_model=MaintenanceResponse)
def create_maintenance(request: MaintenanceCreate, db: Session = Depends(get_db)):
    # Проверка дали гаражът съществува
    garage = db.query(Garage).filter(Garage.id == request.garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")

    # Проверка дали капацитетът на гаража е достатъчен
    if garage.capacity < request.capacity_used:
        raise HTTPException(status_code=400, detail="Insufficient capacity in the garage")

    new_request = Maintenance(**request.dict())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.delete("/{maintenance_id}")
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance request not found")
    db.delete(maintenance)
    db.commit()
    return {"message": "Maintenance request deleted successfully"}
