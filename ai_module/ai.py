import logging
import openai
from openai.types.beta.assistant import Assistant

from settings import settings
from aiogram.types import FSInputFile
from .ai_value_manager import AIValueManager
from .ai_photo_manager import AIPhotoManager
from .ai_config import AI_TOOLS, COMMON_ASSISTANT_INSTRUCTIONS, FILE_SEARCH_INSTRUCTIONS, AI_NAME, GPT_MODEL
from .ai_file_manager import AIFileManager


class AI:
    """Class of AI assistant based on OpenAI"""

    _client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_TOKEN)
    _assistant: Assistant
    _ai_value_manager = AIValueManager(_client)
    ai_photo_manager = AIPhotoManager(_client)
    ai_file_manager = AIFileManager(_client)

    async def init_assistant(self, assistant_id=None):
        """Initialize assistant"""
        try:
            logging.basicConfig(level=logging.INFO)
            if assistant_id is not None:
                AI._assistant = await AI._client.beta.assistants.retrieve(assistant_id=assistant_id)
            else:
                AI._assistant = await AI._client.beta.assistants.create(
                    name=AI_NAME, model=GPT_MODEL,
                    instructions=COMMON_ASSISTANT_INSTRUCTIONS,
                    tools=[AI_TOOLS['SAVE_VALUE']]
                )
            #print(AI._assistant.id)
            self.permission = True
        except openai.PermissionDeniedError:
            self.permission = False

    @classmethod
    async def speech_to_text(cls, file_name: str) -> str:
        """Translate voice file to text"""
        with open(file_name, "rb") as voice_file:
            transcript = await AI._client.audio.transcriptions.create(model="whisper-1", file=voice_file)
            return transcript.text

    @classmethod
    async def text_to_speech(cls, text: str, file_name: str) -> FSInputFile:
        """Translate text to voice file"""
        response = await cls._client.audio.speech.create(model="tts-1", voice="alloy", input=text)
        response.write_to_file(file_name)
        voice_file = FSInputFile(file_name)
        return voice_file

    @classmethod
    async def get_answer(cls, question: str, user_info: dict):
        """Get answer on the question"""
        ai_thread = await AI._client.beta.threads.create()
        await AI._client.beta.threads.messages.create(thread_id=ai_thread.id, role='user', content=question)
        run = await AI._client.beta.threads.runs.create_and_poll(
            thread_id=ai_thread.id, assistant_id=AI._assistant.id, tool_choice='required'
        )

        while run.status in ['completed', 'requires_action', 'failed']:
            logging.info(f"RUN Status: {run.status}")
            if run.status == 'requires_action':
                run, values = await AI._ai_value_manager.get_values(run, ai_thread)
                valid_values = await AI._ai_value_manager.validate_values(values, user_info['user_id'])
                await AI._ai_value_manager.save_values_in_db(user_info['user_id'], valid_values)

            elif run.status == 'completed':
                messages = await AI._client.beta.threads.messages.list(thread_id=ai_thread.id)
                answer = messages.data[0].content[0].text.value
                return answer, True

            elif run.status == 'failed':
                return "The task failed to complete.", False
        else:
            return "The task is still in progress or has an unknown status.", False

    @classmethod
    async def update_assistant(cls):
        vector_store = await cls.ai_file_manager.create_vector_store()

        updated_instructions = f"{cls._assistant.instructions}\n{FILE_SEARCH_INSTRUCTIONS}"
        new_tools = [{"type": "file_search"}]
        updated_tools = cls._assistant.tools + new_tools

        cls.__assistant = await cls._client.beta.assistants.update(
            assistant_id=cls._assistant.id,
            instructions=updated_instructions,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
            tools=updated_tools,
        )
