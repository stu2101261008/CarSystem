from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.car import Car
from app.models.garage import Garage
from app.schemas.car import CarCreate, CarResponse

router = APIRouter()

@router.get("/", response_model=list[CarResponse])
def get_all_cars(db: Session = Depends(get_db)):
    return db.query(Car).all()

@router.get("/{car_id}", response_model=CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.post("/", response_model=CarResponse)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    # Проверка дали сервизът съществува
    if car.garage_id:
        garage = db.query(Garage).filter(Garage.id == car.garage_id).first()
        if not garage:
            raise HTTPException(status_code=404, detail="Garage not found")

    new_car = Car(**car.dict())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

@router.delete("/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(car)
    db.commit()
    return {"message": "Car deleted successfully"}
