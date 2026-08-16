import os
import whisper


model = whisper.load_model("base")


def transcribe_voice(file_path):
    try:
        result = model.transcribe(file_path)

        return result["text"]

    except Exception:
        return None
