from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.ticket import EstadoTicketEnum
 
 
class TicketCreate(BaseModel):
    descripcion: str = Field(..., min_length=10)
    id_servicio: int
 
 
class TicketUpdateEstado(BaseModel):
    estado:      EstadoTicketEnum
    id_asignado: Optional[int] = None   # obligatorio solo al pasar a "asignado"
 
 
class TicketOut(BaseModel):
    id_ticket:           int
    descripcion:         str
    estado:              EstadoTicketEnum
    fecha_creacion:      datetime
    fecha_actualizacion: datetime
    id_solicitante:      int
    id_servicio:         int
    id_asignado:         Optional[int] = None
    model_config = {"from_attributes": True}
 
 
class TicketOutDetalle(TicketOut):
    """Versión enriquecida con nombres relacionales."""
    nombre_solicitante: Optional[str] = None
    nombre_servicio:    Optional[str] = None
    nombre_asignado:    Optional[str] = None
 