import os
from pytube import YouTube
import logging

logger = logging.getLogger(__name__)

def download_video_sync(url: str) -> str:
    try:
        if "youtube.com" in url or "youtu.be" in url:
            logger.info(f"Загружаю видео с YouTube: {url}")
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            file_path = video.download(output_path="downloads")
            return file_path
        else:
            return "Ошибка: Поддерживаются только ссылки с YouTube."
    except Exception as e:
        logger.error(f"Ошибка при загрузке видео: {e}")
        return f"Ошибка при загрузке видео: {e}"
