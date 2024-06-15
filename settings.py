from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


class Settings(BaseSettings):
    openai_api_token: str = Field(env_prefix="OPENAI_API_KEY")
    telegram_bot_token: str = Field(env_prefix="TELEGRAM_BOT_TOKEN")


load_dotenv()
settings = Settings()

AI_TOKEN = settings.openai_api_token
BOT_TOKEN = settings.telegram_bot_token
