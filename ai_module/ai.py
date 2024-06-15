import openai
import time
from settings import AI_TOKEN
from aiogram.types import FSInputFile


class AI:
    """Class of AI assistant based on OpenAI"""
    def __init__(self):
        """Initialize object of AI class"""
        try:
            self.client = openai.OpenAI(api_key=AI_TOKEN)
            self.thread = self.client.beta.threads.create()
            self.permision = True
        except openai.PermissionDeniedError:
            self.permision = False

    def speech_to_text(self, file_name: str) -> str:
        """Translate voice file to text"""
        with open(file_name, "rb") as voice_file:
            transcript = self.client.audio.transcriptions.create(model="whisper-1", file=voice_file)
            return transcript.text

    def text_to_speech(self, text: str, file_name: str = f"answer_{time.time()}") -> FSInputFile:
        """Translate text to voice file"""
        speech_file_name = f"{file_name}.mp3"
        response = self.client.audio.speech.create(model="tts-1", voice="alloy", input=text)
        response.write_to_file(speech_file_name)
        voice_file = FSInputFile(speech_file_name)
        return voice_file

    def get_answer(self, question: str) -> str:
        """Get answer on the question"""
        ai_thread = self.client.beta.threads.create()
        assistant = self.client.beta.assistants.create(name="Jarvis", instructions="", model='gpt-4-1106-preview')
        self.client.beta.threads.messages.create(thread_id=ai_thread.id, role='user', content=question)
        run = self.client.beta.threads.runs.create(thread_id=ai_thread.id, assistant_id=assistant.id)

        while run.status != 'completed':
            run = self.client.beta.threads.runs.retrieve(thread_id=ai_thread.id, run_id=run.id)
            time.sleep(1)

        messages = self.client.beta.threads.messages.list(thread_id=ai_thread.id)
        answer = messages.data[0].content[0].text.value
        return answer
