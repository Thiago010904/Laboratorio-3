from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate
from app.api.deps import require_roles, get_current_user


router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/")
def crear_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("Solicitante"))
):
    nuevo = Ticket(
        descripcion=ticket.descripcion,
        id_servicio=ticket.id_servicio,
        id_solicitante=user.id_usuario
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/")
def ver_tickets(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.rol == "Solicitante":
        return db.query(Ticket).filter(Ticket.id_solicitante == user.id_usuario).all()

    return db.query(Ticket).all()


@router.put("/{ticket_id}/estado")
def cambiar_estado(
    ticket_id: int,
    estado: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    ticket = db.query(Ticket).filter(Ticket.id_ticket == ticket_id).first()

    if not ticket:
        raise HTTPException(404, "Ticket no encontrado")

    
    if user.rol == "Tecnico_Mantenimiento":
        if ticket.id_asignado != user.id_usuario:
            raise HTTPException(403, "No puedes modificar este ticket")

        if estado not in ["en_proceso", "finalizado"]:
            raise HTTPException(400, "Estado no permitido")

    ticket.estado = estado
    ticket.fecha_actualizacion = datetime.utcnow()

    db.commit()
    db.refresh(ticket)

    return ticket