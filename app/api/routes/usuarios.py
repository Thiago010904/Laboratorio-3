from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.services.usuario_service import create_usuario
from app.api.deps import require_roles


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioOut)
def crear_usuario(
    user: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("Administrador"))
):
    return create_usuario(db, user)


@router.get("/me", response_model=UsuarioOut)
def get_me(current_user=Depends(require_roles(
    "Administrador", "Solicitante", "Tecnico_Mantenimiento", "Auxiliar_Laboratorio"
))):
    return current_user