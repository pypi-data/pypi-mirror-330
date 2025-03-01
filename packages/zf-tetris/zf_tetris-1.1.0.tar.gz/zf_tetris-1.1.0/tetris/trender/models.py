from datetime import datetime
from os import path as os_path
from io import BytesIO

from loguru import logger
from pydantic import BaseModel
from requests import get as http_get

from tetris.trender.config import settings
from tetris.trender.minio import minio_client

class RedditPost(BaseModel):
    id: str
    subreddit: str
    creator: str
    title: str
    url: str
    permalink: str
    num_likes: int
    num_comments: int
    num_shares: int
    ratio_likes: float
    created_at: datetime

    def _get_filename(self) -> tuple[str, str]:
        title = self.title.strip().lower().replace(" ", "_")
        ext = self.url.split(".")[-1]
        if ext not in ["jpg", "jpeg", "png", "gif"]:
            ext = "png"
        return title, f"{title}.{ext}"

    def download(self, directory: str | None = None) -> str | None:
        if directory is None:
            raise ValueError("directory is required")

        title, filename = self._get_filename()
        filepath = os_path.join(directory, filename)

        if os_path.exists(filepath):
            logger.warning(f"Download skipping {title}")
            return filepath

        try:
            response = http_get(self.url)

            if response.status_code != 200:
                logger.error(f"Download rejected {title}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Download failed {title}: {e}")
            return None

        with open(filepath, "wb") as f:
            f.write(response.content)

        logger.info(f"Download success {title}")
        return filepath

    def upload(self, bucket: str | None = None) -> str | None:
        if bucket is None:
            raise ValueError("bucket is required")

        title, object_name = self._get_filename()

        bucket_parts = bucket.split("/", 1)
        bucket_name = bucket_parts[0]
        prefix = bucket_parts[1] + "/" if len(bucket_parts) > 1 else ""
        full_object_name = prefix + object_name

        try:
            response = http_get(self.url)
            if response.status_code != 200:
                logger.error(f"Download rejected {title}: {response.status_code}")
                return None

            data = BytesIO(response.content)
            data.seek(0)
            length = len(response.content)

            minio_client.put_object(
                bucket_name=bucket_name,
                object_name=full_object_name,
                data=data,
                length=length,
                content_type=response.headers.get("content-type", "application/octet-stream"),
            )

            logger.info(f"Upload success {title} to MinIO")
            return f"{settings.TETRIS_MINIO_ENDPOINT}/{bucket_name}/{full_object_name}"

        except Exception as e:
            logger.error(f"Upload failed {title}: {e}")
            return None

