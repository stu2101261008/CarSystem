from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import garages

# Създаване на таблиците
Base.metadata.create_all(bind=engine)

# Инициализация на приложението
app = FastAPI()

# Позволяване на CORS (за работа с фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Позволяване на всички домейни
    allow_credentials=True,
    allow_methods=["*"],  # Позволяване на всички методи (GET, POST и т.н.)
    allow_headers=["*"],  # Позволяване на всички хедъри
)

# Регистриране на рутерите
app.include_router(garages.router, prefix="/garages", tags=["Garages"])

@app.get("/")
def root():
    return {"message": "Car Management API is running successfully"}
