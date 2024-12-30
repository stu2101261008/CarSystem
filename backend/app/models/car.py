from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.garage import Garage

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    make = Column(String, nullable=False)  # Марка на колата
    model = Column(String, nullable=False)  # Модел на колата
    production_year = Column(Integer, nullable=False)  # Година на производство
    license_plate = Column(String, unique=True, nullable=False)  # Регистрационен номер
    garage_id = Column(Integer, ForeignKey("garages.id", ondelete="SET NULL"))  # ID на сервиза

    garage = relationship("Garage", back_populates="cars")  # Релация към сервиза
