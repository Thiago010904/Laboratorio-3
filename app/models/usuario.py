import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base

# Definimos los roles exactos que usarán en el sistema
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
    contrasena = Column(String)  # Corregido: ahora coincide con el service
    rol = Column(Enum(RolEnum))  # Corregido: usando la clase Enum real
    activo = Column(Boolean, default=True)

    # Relaciones
    tickets_solicitados = relationship("Ticket", foreign_keys="Ticket.id_solicitante", back_populates="solicitante")
    tickets_responsable = relationship("Ticket", foreign_keys="Ticket.id_responsable", back_populates="responsable")
    tickets_asignados = relationship("Ticket", foreign_keys="Ticket.id_asignado", back_populates="asignado")