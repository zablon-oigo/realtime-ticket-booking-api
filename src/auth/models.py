from __future__ import annotations
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.sql import func
import uuid
from datetime import datetime, timezone
from typing import Optional, List


class User(SQLModel, table=True):
    __tablename__ = "user_accounts"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    )
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified: bool = Field(default=False, sa_column=Column(pg.BOOLEAN, nullable=False, server_default="false"))
    email: str = Field(sa_column=Column(pg.VARCHAR(40), unique=True, nullable=False))
    password_hash: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now())
    )
    events: List["Event"] = Relationship(back_populates="owner_user")
    bookings: List["Booking"] = Relationship(back_populates="user")
    tickets: List["Ticket"] = Relationship(back_populates="booked_by_user")

    def __init__(self, **data):
        if "username" not in data or not data["username"]:
            data["username"] = data.get("email")
        super().__init__(**data)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
