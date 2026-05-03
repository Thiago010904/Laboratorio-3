import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base


class RolEnum(str, enum.Enum):
    administrador = "Administrador"
    solicitante = "Solicitante"
    tecnico_mantenimiento = "Tecnico_Mantenimiento"
    auxiliar_laboratorio = "Auxiliar_Laboratorio"

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True)
    contrasena = Column(String) 
    rol = Column(Enum(RolEnum)) 
    activo = Column(Boolean, default=True)

    # Relaciones
    tickets_solicitados = relationship("Ticket", foreign_keys="Ticket.id_solicitante", back_populates="solicitante")
    tickets_responsable = relationship("Ticket", foreign_keys="Ticket.id_responsable", back_populates="responsable")
    tickets_asignados = relationship("Ticket", foreign_keys="Ticket.id_asignado", back_populates="asignado")