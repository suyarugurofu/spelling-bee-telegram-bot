import json
import os
from bot.config import Config

def load_phrases():
    lang = Config.BOT_LANG or 'en'
    path = os.path.join(os.path.dirname(__file__), 'locales', f'{lang}.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

PHRASES = load_phrases()