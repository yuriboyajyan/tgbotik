import whisper
import logging

logger = logging.getLogger(__name__)

def transcribe_audio_sync(audio_path: str) -> str:
    try:
        model = whisper.load_model("small")
        result = model.transcribe(audio_path)
        logger.info(f"Транскрипция завершена")
        return result["text"]
    except Exception as e:
        logger.error(f"Ошибка при транскрипции: {e}")
        return f"Ошибка при транскрипции: {e}"
