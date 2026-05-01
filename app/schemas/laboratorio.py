from typing import Optional
from pydantic import BaseModel, Field
 
 
class LaboratorioBase(BaseModel):
    nombre:      str           = Field(..., min_length=2, max_length=150)
    ubicacion:   str           = Field(..., min_length=2, max_length=255)
    descripcion: Optional[str] = None
 
 
class LaboratorioCreate(LaboratorioBase):
    pass
 
 
class LaboratorioUpdate(BaseModel):
    nombre:      Optional[str] = Field(None, min_length=2, max_length=150)
    ubicacion:   Optional[str] = Field(None, min_length=2, max_length=255)
    descripcion: Optional[str] = None
 
 
class LaboratorioOut(LaboratorioBase):
    id_laboratorio: int
    model_config = {"from_attributes": True}
 