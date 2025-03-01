from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    TETRIS_REDDIT_CLIENT_ID: str
    TETRIS_REDDIT_CLIENT_SECRET: str
    TETRIS_MINIO_ENDPOINT: str
    TETRIS_MINIO_ACCESS_KEY: str
    TETRIS_MINIO_SECRET_KEY: str
    TETRIS_MINIO_SECURE: bool = False

    model_config = SettingsConfigDict(
        env_file=[
            os.path.join(os.path.dirname(__file__), "..", ".env.dev"),
            os.path.join(os.path.dirname(__file__), "..", ".env.prod")
        ],
        env_file_encoding="utf-8"
    )


settings = Settings()
logger.info(f"Settings: {settings}")
