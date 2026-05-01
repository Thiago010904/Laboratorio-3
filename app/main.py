from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base

# importar modelos para que se creen
from app.models import usuario, laboratorio, servicio, ticket

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"msg": "API funcionando"}