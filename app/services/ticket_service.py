from sqlalchemy.orm import Session
from fastapi import HTTPException, status
 
from app.models.ticket import Ticket, EstadoTicketEnum
from app.models.usuario import Usuario, RolEnum
from app.schemas.ticket import TicketCreate, TicketUpdateEstado, TicketOut, TicketOutDetalle

TRANSICIONES: dict[str, dict[str, list[str]]] = {
    RolEnum.administrador: {
        EstadoTicketEnum.solicitado: [EstadoTicketEnum.recibido,   EstadoTicketEnum.cancelado],
        EstadoTicketEnum.recibido:   [EstadoTicketEnum.asignado,   EstadoTicketEnum.cancelado],
        EstadoTicketEnum.asignado:   [EstadoTicketEnum.en_proceso, EstadoTicketEnum.cancelado],
        EstadoTicketEnum.en_proceso: [EstadoTicketEnum.finalizado, EstadoTicketEnum.cancelado],
    },
    RolEnum.auxiliar_laboratorio: {
        EstadoTicketEnum.solicitado: [EstadoTicketEnum.recibido,   EstadoTicketEnum.cancelado],
        EstadoTicketEnum.recibido:   [EstadoTicketEnum.asignado],
    },
    RolEnum.tecnico_mantenimiento: {
       
        EstadoTicketEnum.asignado:   [EstadoTicketEnum.en_proceso],
        EstadoTicketEnum.en_proceso: [EstadoTicketEnum.finalizado],
    },
    RolEnum.solicitante: {
    
        EstadoTicketEnum.solicitado: [EstadoTicketEnum.cancelado],
    },
}
 
 
# ── Helpers internos ─────────────────────────────────────────────
 
def _get_or_404(db: Session, id_ticket: int) -> Ticket:
    t = db.query(Ticket).filter(Ticket.id_ticket == id_ticket).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket no encontrado.")
    return t
 
 
def _check_acceso_lectura(ticket: Ticket, current_user: Usuario) -> None:
    """Valida que el usuario tenga derecho a leer este ticket."""
    rol = current_user.rol
    if rol == RolEnum.solicitante and ticket.id_solicitante != current_user.id_usuario:
        raise HTTPException(status_code=403, detail="Acceso denegado.")
    if rol == RolEnum.tecnico_mantenimiento and ticket.id_asignado != current_user.id_usuario:
        raise HTTPException(status_code=403, detail="Acceso denegado.")
 
 
def _validar_transicion(
    ticket: Ticket,
    nuevo_estado: EstadoTicketEnum,
    current_user: Usuario,
) -> None:
    """
    Valida que la transición de estado sea permitida según:
    1. La matriz TRANSICIONES para el rol.
    2. Reglas específicas de propiedad (técnico, solicitante).
    """
    rol           = current_user.rol
    estado_actual = ticket.estado
 
    destinos = TRANSICIONES.get(rol, {}).get(estado_actual, [])
    if nuevo_estado not in destinos:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Transición no permitida: '{estado_actual}' → '{nuevo_estado}' "
                f"para el rol '{rol}'."
            ),
        )
 
    # Regla extra: técnico solo mueve sus tickets asignados
    if rol == RolEnum.tecnico_mantenimiento:
        if ticket.id_asignado != current_user.id_usuario:
            raise HTTPException(
                status_code=403,
                detail="Solo puedes modificar tickets asignados a ti.",
            )
 
    # Regla extra: solicitante solo cancela sus propios tickets
    if rol == RolEnum.solicitante:
        if ticket.id_solicitante != current_user.id_usuario:
            raise HTTPException(
                status_code=403,
                detail="Solo puedes modificar tus propios tickets.",
            )
 
 
# ── CRUD / Lógica ────────────────────────────────────────────────
 
def crear_ticket(db: Session, payload: TicketCreate, current_user: Usuario) -> Ticket:
    ticket = Ticket(
        descripcion    = payload.descripcion,
        estado         = EstadoTicketEnum.solicitado,
        id_solicitante = current_user.id_usuario,
        id_servicio    = payload.id_servicio,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
 
 
def listar_tickets(db: Session, current_user: Usuario) -> list[Ticket]:
    rol = current_user.rol
    if rol in (RolEnum.administrador, RolEnum.auxiliar_laboratorio):
        return db.query(Ticket).all()
    if rol == RolEnum.tecnico_mantenimiento:
        return db.query(Ticket).filter(Ticket.id_asignado == current_user.id_usuario).all()
    if rol == RolEnum.solicitante:
        return db.query(Ticket).filter(Ticket.id_solicitante == current_user.id_usuario).all()
    raise HTTPException(status_code=403, detail="Rol sin acceso a tickets.")
 
 
def obtener_ticket_detalle(
    db: Session, id_ticket: int, current_user: Usuario
) -> TicketOutDetalle:
    ticket = _get_or_404(db, id_ticket)
    _check_acceso_lectura(ticket, current_user)
    return TicketOutDetalle(
        **TicketOut.model_validate(ticket).model_dump(),
        nombre_solicitante = ticket.solicitante.nombre if ticket.solicitante else None,
        nombre_servicio    = ticket.servicio.nombre    if ticket.servicio    else None,
        nombre_asignado    = ticket.asignado.nombre    if ticket.asignado    else None,
    )
 
 
def cambiar_estado(
    db: Session,
    id_ticket: int,
    payload: TicketUpdateEstado,
    current_user: Usuario,
) -> Ticket:
    ticket = _get_or_404(db, id_ticket)
    _validar_transicion(ticket, payload.estado, current_user)
 
    # Al asignar, validar que el técnico exista y tenga el rol correcto
    if payload.estado == EstadoTicketEnum.asignado:
        if not payload.id_asignado:
            raise HTTPException(
                status_code=422,
                detail="Debes proporcionar 'id_asignado' para asignar el ticket.",
            )
        tecnico = (
            db.query(Usuario)
            .filter(
                Usuario.id_usuario == payload.id_asignado,
                Usuario.rol == RolEnum.tecnico_mantenimiento,
            )
            .first()
        )
        if not tecnico:
            raise HTTPException(
                status_code=404,
                detail="El técnico no existe o no tiene el rol 'Tecnico_Mantenimiento'.",
            )
        ticket.id_asignado = payload.id_asignado
 
    ticket.estado = payload.estado
    db.commit()
    db.refresh(ticket)
    return ticket
 
 
def eliminar_ticket(db: Session, id_ticket: int) -> None:
    ticket = _get_or_404(db, id_ticket)
    db.delete(ticket)
    db.commit()