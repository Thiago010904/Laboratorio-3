from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Laboratorio(Base):
    __tablename__ = "laboratorios"

    id_laboratorio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    ubicacion = Column(String)
    descripcion = Column(String, nullable=True)
    activo = Column(Boolean, default=True)

    # Relaciones
    tickets = relationship("Ticket", back_populates="laboratorio")
    servicios = relationship("Servicio", back_populates="laboratorio")