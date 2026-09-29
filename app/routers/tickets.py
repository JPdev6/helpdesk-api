from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Ticket, TicketPriority, TicketStatus
from app.schemas import TicketCreate, TicketRead, TicketUpdate

router = APIRouter(prefix="/tickets", tags=["tickets"])


def get_ticket_or_404(ticket_id: int, db: Session) -> Ticket:
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return ticket


@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)) -> Ticket:
    ticket = Ticket(**payload.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("", response_model=list[TicketRead])
def list_tickets(
    status_filter: TicketStatus | None = Query(default=None, alias="status"),
    priority: TicketPriority | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
) -> list[Ticket]:
    stmt = select(Ticket)

    if status_filter is not None:
        stmt = stmt.where(Ticket.status == status_filter)
    if priority is not None:
        stmt = stmt.where(Ticket.priority == priority)
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(Ticket.title.ilike(pattern), Ticket.description.ilike(pattern))
        )

    stmt = stmt.order_by(Ticket.id)
    return list(db.scalars(stmt).all())


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)) -> Ticket:
    return get_ticket_or_404(ticket_id, db)


@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket(
    ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)
) -> Ticket:
    ticket = get_ticket_or_404(ticket_id, db)
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(ticket, field, value)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)) -> None:
    ticket = get_ticket_or_404(ticket_id, db)
    db.delete(ticket)
    db.commit()
