import uuid
import logging
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from ..config import settings

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    return passwd_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)



def create_access_token(
    user_data: dict,
    expiry: timedelta = None,
    refresh: bool = False
) -> str:

    payload = {
        "user": user_data,
        "exp": datetime.utcnow() + (expiry if expiry else timedelta(minutes=60)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh
    }

    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        logging.warning("Token expired.")
        return None
    except jwt.PyJWTError as jwte:
        logging.error(f"JWT decode error: {jwte}")
        return None
    except Exception as e:
        logging.error(f"Unexpected decode error: {e}")
        return None
