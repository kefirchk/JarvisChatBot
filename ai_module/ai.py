import logging
import openai

from settings import settings
from aiogram.types import FSInputFile
from .ai_value_manager import AIValueManager
from .ai_config import AI_TOOLS, ASSISTANT_INSTRUCTIONS, AI_NAME


class AI:
    """Class of AI assistant based on OpenAI"""

    __client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_TOKEN)
    __assistant = None
    __ai_value_manager = AIValueManager(__client)

    async def init_assistant(self, assistant_id):
        """Initialize assistant"""
        try:
            logging.basicConfig(level=logging.INFO)
            if assistant_id is not None:
                self.__assistant = await self.__client.beta.assistants.retrieve(assistant_id=assistant_id)
            else:
                self.__assistant = await self.__client.beta.assistants.create(
                    name=AI_NAME, model='gpt-4',
                    instructions=ASSISTANT_INSTRUCTIONS,
                    tools=[AI_TOOLS['SAVE_VALUE']]
                )
            self.permission = True
        except openai.PermissionDeniedError:
            self.permission = False

    @classmethod
    async def speech_to_text(cls, file_name: str) -> str:
        """Translate voice file to text"""
        with open(file_name, "rb") as voice_file:
            transcript = await AI.__client.audio.transcriptions.create(model="whisper-1", file=voice_file)
            return transcript.text

    @classmethod
    async def text_to_speech(cls, text: str, file_name: str) -> FSInputFile:
        """Translate text to voice file"""
        response = await AI.__client.audio.speech.create(model="tts-1", voice="alloy", input=text)
        response.write_to_file(file_name)
        voice_file = FSInputFile(file_name)
        return voice_file

    async def get_answer(self, question: str, user_info: dict):
        """Get answer on the question"""
        ai_thread = await AI.__client.beta.threads.create()
        await AI.__client.beta.threads.messages.create(thread_id=ai_thread.id, role='user', content=question)
        run = await AI.__client.beta.threads.runs.create_and_poll(
            thread_id=ai_thread.id, assistant_id=self.__assistant.id, tool_choice='required'
        )

        while run.status in ['completed', 'requires_action', 'failed']:
            logging.info(f"RUN Status: {run.status}")
            if run.status == 'requires_action':
                run, values = await AI.__ai_value_manager.get_values(run, ai_thread)
                valid_values = await AI.__ai_value_manager.validate_values(values, user_info['user_id'])
                await AI.__ai_value_manager.save_values_in_db(user_info['user_id'], valid_values)

            elif run.status == 'completed':
                messages = await AI.__client.beta.threads.messages.list(thread_id=ai_thread.id)
                answer = messages.data[0].content[0].text.value
                return answer, True

            elif run.status == 'failed':
                return "The task failed to complete.", False
        else:
            return "The task is still in progress or has an unknown status.", False
