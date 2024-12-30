from pydantic import BaseModel
from typing import Optional

class CarBase(BaseModel):
    make: str
    model: str
    production_year: int
    license_plate: str
    garage_id: Optional[int]  # ID на сервиза (може да бъде null)

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int

    class Config:
        orm_mode = True
