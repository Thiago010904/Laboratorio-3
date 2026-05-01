from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id_ticket = Column(Integer, primary_key=True)

    id_solicitante = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_responsable = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    id_asignado = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)

    id_laboratorio = Column(Integer, ForeignKey("laboratorios.id_laboratorio"))
    id_servicio = Column(Integer, ForeignKey("servicios.id_servicio"))

    titulo = Column(String)
    descripcion = Column(String)

    estado = Column(String, default="solicitado")
    prioridad = Column(String)

    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    solicitante = relationship("Usuario", foreign_keys=[id_solicitante])
    responsable = relationship("Usuario", foreign_keys=[id_responsable])
    asignado = relationship("Usuario", foreign_keys=[id_asignado])

    laboratorio = relationship("Laboratorio")
    servicio = relationship("Servicio")