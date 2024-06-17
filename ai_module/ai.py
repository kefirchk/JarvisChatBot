import openai
from settings import AI_TOKEN
from aiogram.types import FSInputFile


class AI:
    """Class of AI assistant based on OpenAI"""

    __client = openai.AsyncOpenAI(api_key=AI_TOKEN)
    __assistant = None

    def __init__(self):
        """Initialize object of AI class"""
        self.permission = True

    async def init_assistant(self):
        """Initialize assistant"""
        try:
            self.__assistant = await self.__client.beta.assistants.create(
                name="Jarvis", instructions="", model='gpt-4-1106-preview')
        except openai.PermissionDeniedError:
            self.permission = False

    async def speech_to_text(self, file_name: str) -> str:
        """Translate voice file to text"""
        with open(file_name, "rb") as voice_file:
            transcript = await AI.__client.audio.transcriptions.create(model="whisper-1", file=voice_file)
            return transcript.text

    async def text_to_speech(self, text: str, file_name: str) -> FSInputFile:
        """Translate text to voice file"""
        response = await AI.__client.audio.speech.create(model="tts-1", voice="alloy", input=text)
        response.write_to_file(file_name)
        voice_file = FSInputFile(file_name)
        return voice_file

    async def get_answer(self, question: str):
        """Get answer on the question"""
        ai_thread = await AI.__client.beta.threads.create()
        await AI.__client.beta.threads.messages.create(thread_id=ai_thread.id, role='user', content=question)
        run = await AI.__client.beta.threads.runs.create_and_poll(thread_id=ai_thread.id, assistant_id=self.__assistant.id)

        if run.status in ['completed', 'requires_action', 'failed']:
            if run.status == 'completed':
                messages = await AI.__client.beta.threads.messages.list(thread_id=ai_thread.id)
                answer = messages.data[0].content[0].text.value
                return answer, True
            elif run.status == 'requires_action':
                return "The task requires further action.", False
            elif run.status == 'failed':
                return "The task failed to complete.", False
        else:
            return "The task is still in progress or has an unknown status.", False
