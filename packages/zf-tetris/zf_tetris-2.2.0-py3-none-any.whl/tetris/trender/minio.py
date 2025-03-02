from minio import Minio

from tetris.trender.config import settings

minio_client = Minio(
    settings.TETRIS_MINIO_ENDPOINT,
    access_key=settings.TETRIS_MINIO_ACCESS_KEY,
    secret_key=settings.TETRIS_MINIO_SECRET_KEY,
    secure=settings.TETRIS_MINIO_SECURE,
)
