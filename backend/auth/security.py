from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from backend.config.settings import settings


password_hash = PasswordHash.recommended()


def hash_password(
    password: str
) -> str:

    return password_hash.hash(
        password
    )


def verify_password(
    password: str,
    hashed_password: str
) -> bool:

    return password_hash.verify(
        password,
        hashed_password
    )


def create_access_token(
    user_id: int,
    email: str,
    role: str
) -> str:

    expiration = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "exp": expiration
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )