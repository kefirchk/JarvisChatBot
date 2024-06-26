import io
import os

from aiogram import Bot
from aiogram.types import Voice, PhotoSize
from pydub import AudioSegment
import base64

class BotFileManager:
    """Class for file operations by bot"""
    @staticmethod
    async def get_voice_file(bot: Bot, voice: Voice) -> str:
        """Receive .ogg-file (voice) and save the voice as .wav-file."""
        file = await bot.get_file(voice.file_id)
        ogg_file = io.BytesIO()

        await bot.download_file(file.file_path, ogg_file)
        wav_file_name = f"question_{voice.file_unique_id}.wav"

        AudioSegment.from_file(ogg_file, format="ogg").export(wav_file_name, format="wav")
        return wav_file_name

    @staticmethod
    async def remove_files(file_names: list[str]) -> None:
        """Remove files from workspace"""
        for fn in file_names:
            if os.path.exists(fn):
                os.remove(fn)

    @classmethod
    async def get_photo_file(cls, bot: Bot, photo: list[PhotoSize]):
        """Receive a photo from user and save the photo as .jpg file."""
        photo_file_name = f'photo_{photo[-1].file_unique_id}.jpg'

        photo_file = await bot.get_file(photo[-1].file_id)
        await bot.download_file(photo_file.file_path, photo_file_name)

        return photo_file_name

    @classmethod
    async def encode_image(cls, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
