import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
    AUDIO_DIR = "/app/audio"
    BOT_LANG = os.getenv("BOT_LANG", "en")