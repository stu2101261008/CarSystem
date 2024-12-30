from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Maintenance(Base):
    __tablename__ = "maintenances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    garage_id = Column(Integer, ForeignKey("garages.id", ondelete="CASCADE"), nullable=False)
    request_date = Column(Date, nullable=False)  # Дата на заявката
    capacity_used = Column(Integer, nullable=False)  # Използван капацитет

    garage = relationship("Garage", back_populates="maintenances")
