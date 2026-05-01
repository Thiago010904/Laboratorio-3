from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import get_db
from app.models.usuario import Usuario
from app.core.security import verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.correo == form_data.username).first()

    if not user or not verify_password(form_data.password, user.contrasena):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    token = create_access_token({
        "sub": user.correo,
        "id_usuario": user.id_usuario,
        "rol": user.rol
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }