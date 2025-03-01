from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TETRIS_PATH: str
    TETRIS_REDDIT_CLIENT_ID: str
    TETRIS_REDDIT_CLIENT_SECRET: str
    TETRIS_OPENAI_API_KEY: str
    TETRIS_TWITTER_BEARER_TOKEN: str

    model_config = SettingsConfigDict(env_file=(".env.dev", ".env.prod"), env_file_encoding="utf-8")


settings = Settings()
logger.info(f"Settings: {settings}")
