from gtts import gTTS
import os, time

def generate_audio(summary_text, symbol):
    # Ensure audio folder exists
    audio_dir = os.path.join("static", "audio")
    os.makedirs(audio_dir, exist_ok=True)

    if not summary_text or summary_text.strip() == "":
        summary_text = "No summary text available for this stock."

    filename = f"{symbol}_{int(time.time())}.mp3"
    filepath = os.path.join(audio_dir, filename)

    try:
        tts = gTTS(summary_text)
        tts.save(filepath)
        return f"/static/audio/{filename}"
    except Exception as e:
        print("⚠️ TTS generation failed:", e)
        return None
