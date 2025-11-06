from gtts import gTTS
import os
import time

def generate_audio(summary_text, symbol, output_dir="static/audio"):
    os.makedirs(output_dir, exist_ok=True)

    if not summary_text or summary_text.strip() == "":
        summary_text = "No summary text available for this stock."

    filename = f"{symbol}_{int(time.time())}.mp3"
    filepath = os.path.join(output_dir, filename)

    try:
        tts = gTTS(summary_text)
        tts.save(filepath)
        return filepath
    except Exception:
        return None

