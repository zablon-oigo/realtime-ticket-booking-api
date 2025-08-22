from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None


class UserRead(UserBase):
    uid: uuid.UUID


class EventBase(BaseModel):
    event_name: str
    event_description: str
    event_location: str
    event_image: Optional[str] = None
    event_price: float
    event_capacity: int
    event_date: datetime
    booking_start: datetime
    booking_end: datetime
    is_cancelled: bool = False


class BookingBase(BaseModel):
    event_id: uuid.UUID
    ticket_id: Optional[uuid.UUID] = None


class TicketBase(BaseModel):
    event_id: uuid.UUID
    ticket_number: int 


class EventCreate(EventBase):
    pass


class BookingCreate(BookingBase):
    pass


class TicketCreate(TicketBase):
    pass 

class EventUpdate(BaseModel):
    event_name: Optional[str] = None
    event_description: Optional[str] = None
    event_location: Optional[str] = None
    event_image: Optional[str] = None
    event_price: Optional[float] = None
    event_capacity: Optional[int] = None
    event_date: Optional[datetime] = None
    booking_start: Optional[datetime] = None
    booking_end: Optional[datetime] = None
    is_cancelled: Optional[bool] = None 

class TicketRead(TicketBase):
    id: uuid.UUID
    is_booked: bool
    is_paid: bool
    booked_by: Optional[uuid.UUID]
    booked_by_user: Optional[UserRead] = None   
    timestamp: datetime