from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base

# 1. IMPORTACIÓN DE MODELOS
# Es obligatorio importarlos aquí para que SQLAlchemy los detecte
from app.models.usuario import Usuario
from app.models.laboratorio import Laboratorio
from app.models.servicio import Servicio
from app.models.ticket import Ticket

# 2. CREACIÓN DE TABLAS
# Al leer los modelos de arriba, esta línea va a PostgreSQL y crea las tablas físicas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Tickets - Base de Datos",
    version="1.0.0"
)

@app.get("/", tags=["Inicio"])
def root():
    return {
        "status": "online",
        "message": "API funcionando y tablas sincronizadas con PostgreSQL en el esquema jwt_grupo_7"
    }