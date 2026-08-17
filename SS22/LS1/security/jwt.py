import os

from dotenv import load_dotenv

load_dotenv

from datetime import datetime, timedelta, timezone

import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def generate_access_token(username: str):
    now = datetime.now(timezone.utc)

    explite_time = now + timedelta(minutes=30)

    payload = {
        "sub": username,
        "iat": now.timestamp(),
        "exp": explite_time 
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    return jwt.decode(
        token,
        SECRET_KEY,
        [ALGORITHM]
    )
    

# print(generate_access_token("liam"))
print(f"Test 3: {generate_access_token("PhamHongPhong")}")