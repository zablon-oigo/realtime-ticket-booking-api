from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
import uuid


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    event_name: str
    event_description: str
    owner: Optional[uuid.UUID] = Field(default=None, foreign_key="user_accounts.uid")
    event_location: str
    event_image: Optional[str] = None
    event_price: float
    event_capacity: int
    event_date: datetime
    booking_start: datetime
    booking_end: datetime
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_cancelled: bool = Field(default=False)

    bookings: List["Booking"] = Relationship(back_populates="event")
    tickets: List["Ticket"] = Relationship(back_populates="event")


class Booking(SQLModel, table=True):
    __tablename__ = "bookings"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user_accounts.uid")
    event_id: Optional[uuid.UUID] = Field(default=None, foreign_key="events.id")
    ticket_id: Optional[uuid.UUID] = Field(default=None, foreign_key="tickets.id")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    event: Optional[Event] = Relationship(back_populates="bookings")
    ticket: Optional["Ticket"] = Relationship(back_populates="booking")


class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    event_id: Optional[uuid.UUID] = Field(default=None, foreign_key="events.id")
    ticket_number: int
    is_booked: bool = Field(default=False)
    is_paid: bool = Field(default=False)
    booked_by: Optional[uuid.UUID] = Field(default=None, foreign_key="user_accounts.uid")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    event: Optional[Event] = Relationship(back_populates="tickets")
    booking: Optional[Booking] = Relationship(back_populates="ticket")
