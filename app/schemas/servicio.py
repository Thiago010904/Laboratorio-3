from typing import Optional
from pydantic import BaseModel, Field
 
 
class ServicioBase(BaseModel):
    nombre:         str           = Field(..., min_length=2, max_length=150)
    descripcion:    Optional[str] = None
    id_laboratorio: int
 
 
class ServicioCreate(ServicioBase):
    pass
 
 
class ServicioUpdate(BaseModel):
    nombre:         Optional[str] = Field(None, min_length=2, max_length=150)
    descripcion:    Optional[str] = None
    id_laboratorio: Optional[int] = None
 
 
class ServicioOut(ServicioBase):
    id_servicio: int
    model_config = {"from_attributes": True}
 