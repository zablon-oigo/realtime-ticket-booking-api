from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
import uuid

class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    eventName: str
    eventDescription: str
    owner: Optional[uuid.UUID] = Field(default=None, foreign_key="user_accounts.uid")
    eventLocation: str
    eventImage: Optional[str] = None
    eventPrice: float
    eventCapacity: int
    eventDate: datetime
    bookingStart: datetime
    bookingEnd: datetime
    timestamp: datetime
    isCancelled: bool = False



class Booking(SQLModel, table=True):
    __tablename__ = "bookings"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    userId: Optional[uuid.UUID] = Field(default=None, foreign_key="user_accounts.uid")
    eventId: Optional[str] = Field(default=None, foreign_key="events.id")  
    ticketNumber: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    eventId: Optional[str] = Field(default=None, foreign_key="events.id") 
    ticketNumber: int
    isBooked: bool = False
    isPaid: bool = False
    bookedBy: Optional[uuid.UUID] = Field(default=None, foreign_key="user_accounts.uid")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


