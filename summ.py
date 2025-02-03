from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text_sync(text: str) -> str:
    try:
        summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
        logger.info("Конспект создан")
        return summary[0]["summary_text"]
    except Exception as e:
        logger.error(f"Ошибка при создании конспекта: {e}")
        return f"Ошибка при создании конспекта: {e}"
