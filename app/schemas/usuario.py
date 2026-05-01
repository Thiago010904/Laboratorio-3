from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.usuario import RolEnum
 
class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    correo: EmailStr
    rol: RolEnum
 
 
class UsuarioCreate(UsuarioBase):
    contrasena: str = Field(..., min_length=6, max_length=128)
 
 
class UsuarioUpdate(BaseModel):
    nombre:     Optional[str]      = Field(None, min_length=2, max_length=150)
    correo:     Optional[EmailStr] = None
    rol:        Optional[RolEnum]  = None
    contrasena: Optional[str]      = Field(None, min_length=6, max_length=128)
 
 
class UsuarioOut(UsuarioBase):
    id_usuario: int
    model_config = {"from_attributes": True}
 
 
# ── Auth ─────────────────────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
 
 
class TokenData(BaseModel):
    sub:        Optional[str] = None   # correo del usuario
    id_usuario: Optional[int] = None
    rol:        Optional[str] = None
    scopes:     list[str]     = []
 