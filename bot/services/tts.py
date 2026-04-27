import os
from gtts import gTTS
from pydub import AudioSegment
from bot.config import Config

def get_voice_path(word: str, accent: str = 'com') -> str:
    safe_word = "".join(c if c.isalnum() or c in " _-" else "_" for c in word)
    filename_base = f"{safe_word}_{accent}"
    
    ogg_path = os.path.join(Config.AUDIO_DIR, f"{filename_base}.ogg")
    
    if os.path.exists(ogg_path):
        return ogg_path

    mp3_path = os.path.join(Config.AUDIO_DIR, f"{filename_base}.mp3")
    
    try:
        tts = gTTS(text=word, lang='en', tld=accent, slow=False)
        tts.save(mp3_path)

        audio = AudioSegment.from_mp3(mp3_path)
        audio = audio.set_frame_rate(24000).set_channels(1)
        audio.export(ogg_path, format="ogg", codec="libopus")

        os.remove(mp3_path)

    except Exception as e:
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
        if os.path.exists(ogg_path):
            os.remove(ogg_path)
        raise e

    return ogg_path
