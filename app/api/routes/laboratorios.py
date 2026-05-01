from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.laboratorio import Laboratorio
from app.api.deps import require_roles


router = APIRouter(prefix="/laboratorios", tags=["Laboratorios"])


@router.get("/")
def listar_laboratorios(db: Session = Depends(get_db)):
    return db.query(Laboratorio).all()


@router.post("/")
def crear_laboratorio(
    lab: dict,
    db: Session = Depends(get_db),
    user=Depends(require_roles("Administrador"))
):
    nuevo = Laboratorio(**lab)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo