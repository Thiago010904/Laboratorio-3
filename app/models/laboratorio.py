from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Laboratorio(Base):
    __tablename__ = "laboratorios"

    id_laboratorio = Column(Integer, primary_key=True)
    nombre = Column(String)
    ubicacion = Column(String)
    activo = Column(Boolean, default=True)

    tickets = relationship("Ticket")