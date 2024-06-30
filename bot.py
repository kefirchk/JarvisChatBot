import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from settings import settings
from bot_module import BotFileManager
from ai_module import AI
from amplitude_module import AmplitudeEventTracker


bot = Bot(settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
ai = AI()
event_tracker = AmplitudeEventTracker()


@dp.message(F.text == "/start")
async def start_handler(message: Message):
    """Say hello to the user."""
    event_tracker.track_event("Start bot", str(message.from_user.id))
    await message.answer(f"Hello, {message.from_user.first_name}")


@dp.message(F.photo)
async def photo_message_handler(message: Message):
    logging.info("Get photo file")
    photo_file_name = await BotFileManager.get_photo_file(bot, message.photo)

    logging.info("Get mood by photo")
    mood_text = await AI.ai_photo_manager.get_mood_by_photo(photo_file_name)
    if mood_text is not None:
        logging.info("Text of mood to speech translation")
        mood_voice = await ai.text_to_speech(text=mood_text, file_name=photo_file_name)

        logging.info("Send voice of mood")
        await bot.send_voice(message.chat.id, mood_voice, reply_to_message_id=message.message_id)
    else:
        await message.reply("Unfortunately, I can't determine the mood in the photo")

    event_tracker.track_event("Mood by photo", str(message.from_user.id))
    await BotFileManager.remove_files([photo_file_name])


@dp.message(F.voice)
async def voice_message_handler(message: Message):
    """Receives voice messages and answers to them."""
    file_names = []
    user_info = {
        'user_id': message.from_user.id,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }

    logging.info(f'Get voice file from {message.from_user.first_name} {message.from_user.last_name}')
    question_file_name = await BotFileManager.get_voice_file(bot, message.voice)
    file_names.append(question_file_name)
    try:
        if ai.permission is False:
            raise Exception("Unfortunately, using a chatbot is prohibited in your region :(")

        temp_bot_message = await message.answer("I'm thinking about the answer...")

        logging.info(f'Convert question from voice file to text')
        text_question = await ai.speech_to_text(question_file_name)

        logging.info(f'Answer the question')
        text_answer, answer_status = await ai.get_answer(text_question, user_info)
        if answer_status is True:
            logging.info(f'Convert answer from text to voice file')
            answer_file_name = f"answer_{message.voice.file_unique_id}.mp3"
            file_names.append(answer_file_name)
            voice_answer = await ai.text_to_speech(text=text_answer, file_name=answer_file_name)

            logging.info(f'Send voice answer to {message.from_user.first_name} {message.from_user.last_name}')
            await bot.send_voice(chat_id=message.chat.id, voice=voice_answer, reply_to_message_id=message.message_id)
        else:  # Run status is false (error)
            logging.error(f'Run error: {text_answer}')
            await message.reply("Unfortunately, I can't answer your question")

        logging.info(f'Remove last bot message')
        await bot.delete_message(chat_id=message.chat.id, message_id=temp_bot_message.message_id)
    except Exception as e:
        logging.error(f'Exception: {str(e)}')
        await message.reply(str(e))
    finally:
        event_tracker.track_event("Voice question", str(message.from_user.id))

        logging.info(f'Remove temporary files with such extensions as .wav, .mp3')
        await BotFileManager.remove_files(file_names)


@dp.message()
async def default_handler(message: Message):
    """Handler for all unidentified commands."""
    event_tracker.track_event("Unknown command", str(message.from_user.id))
    await message.answer("I don't understand u :(\nSend me voice message")


async def main():
    await ai.init_assistant(settings.ASSISTANT_ID)
    await ai.update_assistant()
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
