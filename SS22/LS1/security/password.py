from traceback import print_tb

import bcrypt


def hass_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()

    hass_pass = bcrypt.hashpw(
        plain_password.encode("utf-8"),
        salt
    )

    return hass_pass.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
    

print(f"Test 1: {hass_password("ConChoDung")}")
print(f"Test 2: {verify_password("ConChoDung", "$2b$12$.jDV1ghDTbaD2/yU26OUleZIFQCGZyp3yvEbOIovifGDdudN1ghbC")}")