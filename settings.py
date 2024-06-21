from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


class Settings(BaseSettings):
    OPENAI_API_TOKEN: str = Field(env_prefix="OPENAI_API_KEY")
    TELEGRAM_BOT_TOKEN: str = Field(env_prefix="TELEGRAM_BOT_TOKEN")
    ASSISTANT_ID: str = Field(env_prefix="ASSISTANT_ID")

    DB_HOST: str = Field(env_prefix="DB_HOST")
    DB_PORT: str = Field(env_prefix="DB_PORT")
    DB_USER: str = Field(env_prefix="DB_USER")
    DB_PASS: str = Field(env_prefix="DB_PASS")
    DB_NAME: str = Field(env_prefix="DB_NAME")

    @property
    def DATABASE_URL_asyncpg(self):
        # DSN
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


load_dotenv()
settings = Settings()
