from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


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


