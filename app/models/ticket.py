import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

# Definimos los estados exactos del flujo
class EstadoTicketEnum(str, enum.Enum):
    solicitado = "solicitado"
    recibido = "recibido"
    asignado = "asignado"
    en_proceso = "en_proceso"
    finalizado = "finalizado"
    cancelado = "cancelado"

class Ticket(Base):
    __tablename__ = "tickets"

    id_ticket = Column(Integer, primary_key=True, index=True)

    id_solicitante = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_responsable = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    id_asignado = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)

    id_laboratorio = Column(Integer, ForeignKey("laboratorios.id_laboratorio"), nullable=True)
    id_servicio = Column(Integer, ForeignKey("servicios.id_servicio"))

    descripcion = Column(String)
    estado = Column(Enum(EstadoTicketEnum), default=EstadoTicketEnum.solicitado)
    prioridad = Column(String, nullable=True)

    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    solicitante = relationship("Usuario", foreign_keys=[id_solicitante], back_populates="tickets_solicitados")
    responsable = relationship("Usuario", foreign_keys=[id_responsable], back_populates="tickets_responsable")
    asignado = relationship("Usuario", foreign_keys=[id_asignado], back_populates="tickets_asignados")

    laboratorio = relationship("Laboratorio", back_populates="tickets")
    servicio = relationship("Servicio", back_populates="tickets")