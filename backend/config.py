import os
import redis
from dotenv import load_dotenv


load_dotenv()


class Configuration:
    DB_URI = os.getenv("MONGO_URI")
    SERVER_URL = os.getenv("SERVER_URL")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    VK_TOKEN = os.getenv("VK_BOT_TOKEN")
    VK_SECRET = os.getenv("VK_SECRET_KEY")
    VK_CONFIRMATION_CODE = os.getenv("VK_CONFIRM_CODE")
    OPERATOR_SK = os.getenv("OPERATOR_SECRET_KEY")


class AppConfig:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
