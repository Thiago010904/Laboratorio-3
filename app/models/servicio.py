from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Servicio(Base):
    __tablename__ = "servicios"

    id_servicio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String, nullable=True)
    
    # Faltaba esta llave foránea fundamental
    id_laboratorio = Column(Integer, ForeignKey("laboratorios.id_laboratorio")) 
    activo = Column(Boolean, default=True)

    # Relaciones
    laboratorio = relationship("Laboratorio", back_populates="servicios")
    tickets = relationship("Ticket", back_populates="servicio")