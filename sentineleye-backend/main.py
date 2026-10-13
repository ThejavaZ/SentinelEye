import uvicorn as uv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import settings
from core.database import engine, Base

# Importar modelos para que SQLAlchemy los reconozca al crear las tablas
from modules.auth.models import User
from modules.cameras.models import Zone, Camera
from modules.incidents.models import Incident

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, restringe esto a los dominios o apps permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar la carpeta estática para servir las capturas de evidencia (snapshots)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Registrar los routers de los módulos
# app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
# app.include_router(cameras_router, prefix="/api/cameras", tags=["Cameras"])
# app.include_router(incidents_router, prefix="/api/incidents", tags=["Incidents"])

@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "message": "Industrial Security Monitoring AI Backend is running."
    }
    
def main():
    uv.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )

if __name__ == "__main__":
    main()