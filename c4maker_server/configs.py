import os

DB_URL = os.getenv("DB_URL", "localhost:3306/c4_maker")
DB_USERNAME = os.getenv("DB_USERNAME", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DB_CONNECTION_STR = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}"

VERSION = "1.0"

ENCRYPT_SECRET_KEY = os.getenv("ENCRYPT_SECRET_KEY", "")
HOURS_TO_EXPIRATION_TOKEN = int(os.getenv("HOURS_TO_EXPIRATION_TOKEN", "12"))

HOST_PORT = 5000
