from fastapi import FastAPI

# ROUTES
from app.api.routes import auth, usuarios, tickets, laboratorios, servicios



app = FastAPI(
    title="Sistema de Gestión de Tickets - Base de Datos",
    version="1.0.0"
)

@app.get("/", tags=["Inicio"])
def root():
    return {
        "status": "online",
        "message": "API funcionando correctamente"
    }

# REGISTRAR ROUTERS
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tickets.router)
app.include_router(laboratorios.router)
app.include_router(servicios.router)