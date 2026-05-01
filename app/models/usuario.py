from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True)
    password_hash = Column(String)
    rol = Column(String)
    activo = Column(Boolean, default=True)

    tickets_solicitados = relationship("Ticket", foreign_keys="Ticket.id_solicitante")
    tickets_responsable = relationship("Ticket", foreign_keys="Ticket.id_responsable")
    tickets_asignados = relationship("Ticket", foreign_keys="Ticket.id_asignado")