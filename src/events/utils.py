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

