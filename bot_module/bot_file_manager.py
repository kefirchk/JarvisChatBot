import io
import os
import glob

from aiogram import Bot
from aiogram.types import Voice
from pydub import AudioSegment


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
    def remove_voice_files() -> None:
        """Remove files with such extensions as .wav, .mp3"""
        for file in glob.glob("*.wav") + glob.glob("*.mp3"):
            os.remove(file)
