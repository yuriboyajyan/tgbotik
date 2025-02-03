import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from download import download_video_sync
from download import extract_audio_sync
from trscribe import transcribe_audio_sync
from summ import summarize_text_sync
from util import run_in_executor

TOKEN = os.getenv("7724643454:AAHj11qbCkSKtSUEgGuSCZhisrTMoCtBGLs")

dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply("Привет! Отправь мне ссылку на видео, и я создам конспект.")

@dp.message(F.text)
async def handle_video_url(message: types.Message):
    url = message.text.strip()
    if not url.startswith(('http://', 'https://')):
        await message.reply("Пожалуйста, отправьте правильную ссылку на видео.")
        return

    await message.reply("Обрабатываю видео...")

    video_path = await run_in_executor(download_video_sync, url)
    if "Ошибка" in video_path:
        await message.reply(video_path)
        return

    audio_path = await run_in_executor(extract_audio_sync, video_path)
    if "Ошибка" in audio_path:
        await message.reply(audio_path)
        return

    text = await run_in_executor(transcribe_audio_sync, audio_path)
    if "Ошибка" in text:
        await message.reply(text)
        return

    summary = await run_in_executor(summarize_text_sync, text)
    if "Ошибка" in summary:
        await message.reply(summary)
        return

    await message.reply(f"Готово!\n\n{summary}")

    for file_path in [video_path, audio_path]:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Ошибка при удалении файла {file_path}: {e}")

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
