from sqlalchemy.orm import Session
from fastapi import HTTPException, status
 
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import hash_password


def get_by_id(db: Session, id_usuario: int) -> Usuario:
    u = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return u
 
 
def get_by_correo(db: Session, correo: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.correo == correo).first()
 
 
def get_all(db: Session) -> list[Usuario]:
    return db.query(Usuario).all()
 
 
def create(db: Session, payload: UsuarioCreate) -> Usuario:
    if get_by_correo(db, payload.correo):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario registrado con ese correo.",
        )
    usuario = Usuario(
        nombre     = payload.nombre,
        correo     = payload.correo,
        contrasena = hash_password(payload.contrasena),
        rol        = payload.rol,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
 
 
def update(db: Session, id_usuario: int, payload: UsuarioUpdate) -> Usuario:
    usuario = get_by_id(db, id_usuario)
    datos = payload.model_dump(exclude_unset=True)
    if "contrasena" in datos:
        datos["contrasena"] = hash_password(datos.pop("contrasena"))
    for campo, valor in datos.items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario
 
 
def delete(db: Session, id_usuario: int, current_id: int) -> None:
    if id_usuario == current_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta.",
        )
    usuario = get_by_id(db, id_usuario)
    db.delete(usuario)
    db.commit()
 