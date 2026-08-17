import os
from dotenv import load_dotenv

load_dotenv()

MEDCARE_SECRET_KEY = os.getenv("MEDCARE_SECRET_KEY")

if not MEDCARE_SECRET_KEY:
    raise RuntimeError("MEDCARE_SECRET_KEY chưa được cấu hình")