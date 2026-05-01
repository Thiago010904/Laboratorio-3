from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.servicio import Servicio
from app.api.deps import require_roles

router = APIRouter(prefix="/servicios", tags=["Servicios"])


@router.get("/")
def listar_servicios(db: Session = Depends(get_db)):
    return db.query(Servicio).all()


@router.post("/")
def crear_servicio(
    servicio: dict,
    db: Session = Depends(get_db),
    user=Depends(require_roles("Administrador"))
):
    nuevo = Servicio(**servicio)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo