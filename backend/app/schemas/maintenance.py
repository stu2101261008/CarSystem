from pydantic import BaseModel
from datetime import date

class MaintenanceBase(BaseModel):
    garage_id: int
    request_date: date
    capacity_used: int

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceResponse(MaintenanceBase):
    id: int

    class Config:
        orm_mode = True
