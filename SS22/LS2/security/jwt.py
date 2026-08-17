from datetime import datetime, timedelta, timezone

import jwt

from config import MEDCARE_SECRET_KEY


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


def create_access_token(username: str, role: str) -> str:
    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role": role,
        "iat": now,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        MEDCARE_SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return token


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        MEDCARE_SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    return payload