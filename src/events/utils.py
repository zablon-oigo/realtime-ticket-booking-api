import uuid
import logging
from datetime import datetime, timedelta
from typing import Optional, Union

from .schemas import (
    EventCreate,
    EventRead,
    BookingCreate,
    BookingRead,
    TicketCreate,
    TicketRead,
    UserRead,
)

logger = logging.getLogger(__name__)


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()

def current_timestamp() -> datetime:
    return datetime.utcnow()

def create_event(
    event_data: EventCreate,
    owner_id: Optional[uuid.UUID] = None,
) -> EventRead:
    event_id = generate_uuid()
    timestamp = current_timestamp()

    logger.info(f"Creating new event: {event_data.event_name} ({event_id})")
