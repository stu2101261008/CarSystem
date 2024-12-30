from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.garage import Garage
from app.schemas.garage import GarageCreate, GarageResponse
from fastapi import Query

router = APIRouter()


@router.get("/", response_model=list[GarageResponse])
def get_all_garages(city: str = Query(None), db: Session = Depends(get_db)):
    """
    Извлича списък с гаражи. 
    Може да се филтрира по град (city).
    """
    query = db.query(Garage)
    if city:  # Ако параметърът city е подаден
        query = query.filter(Garage.city.ilike(f"%{city}%"))
    return query.all()



@router.get("/", response_model=list[GarageResponse])
def get_all_garages(db: Session = Depends(get_db)):
    return db.query(Garage).all()

@router.get("/{garage_id}", response_model=GarageResponse)
def get_garage(garage_id: int, db: Session = Depends(get_db)):
    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return garage

@router.post("/", response_model=GarageResponse)
def create_garage(garage: GarageCreate, db: Session = Depends(get_db)):
    new_garage = Garage(**garage.dict())
    db.add(new_garage)
    db.commit()
    db.refresh(new_garage)
    return new_garage

@router.delete("/{garage_id}")
def delete_garage(garage_id: int, db: Session = Depends(get_db)):
    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    db.delete(garage)
    db.commit()
    return {"message": "Garage deleted successfully"}
