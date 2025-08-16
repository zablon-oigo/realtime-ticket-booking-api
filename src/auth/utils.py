import uuid
import logging
from datetime import datetime, timedelta
from typing import Optional, Union

import jwt
from passlib.context import CryptContext

from ..config import settings

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return passwd_context.verify(password, hashed_password)


def create_access_token(
    user_data: dict,
    expiry: Optional[timedelta] = None,
    refresh: bool = False
) -> str:
    expiry = expiry or timedelta(minutes=getattr(settings, "JWT_EXPIRY_MINUTES", 60))
    payload = {
        "sub": str(user_data.get("id")),  
        "user": user_data,               
        "exp": datetime.utcnow() + expiry,
        "jti": str(uuid.uuid4()),        
        "refresh": refresh
    }

    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"require": ["exp", "jti"]}
        )
    except jwt.ExpiredSignatureError:
        logging.warning("JWT token expired.")
    except jwt.InvalidTokenError as jwte:
        logging.error(f"JWT decode error: {jwte}")
    except Exception as e:
        logging.error(f"Unexpected decode error: {e}")
    return None
