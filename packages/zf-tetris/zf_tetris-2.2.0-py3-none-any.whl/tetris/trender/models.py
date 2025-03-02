from __future__ import annotations
from datetime import datetime
from os import path as os_path
from io import BytesIO
import json

from loguru import logger
from pydantic import BaseModel
from requests import get as http_get

from tetris.trender.minio import minio_client

class RedditPost(BaseModel):
    id: str
    subreddit: str
    creator: str
    media_type: str | None
    title: str | None # None for comments
    content: str | None
    comments: list[RedditPost] | None
    url: str
    permalink: str
    num_likes: int
    num_comments: int | None # None for comments
    num_shares: int | None # None for comments
    ratio_likes: float | None # None for comments
    created_at: datetime


    def _get_filename(self) -> tuple[str, str]:
        title = self.title.strip().lower().replace(" ", "_")

        if self.media_type == "image":
            ext = "jpg"
        elif self.media_type == "gif":
            ext = "gif"
        elif self.media_type == "video":
            ext = "mp4"
        elif self.media_type == "gallery":
            ext = "jpg"
        elif self.media_type == "link":
            ext = "png"
        elif self.content is not None:
            ext = "json"
        else:
            ext = self.url.split(".")[-1]
            if ext not in ["jpg", "jpeg", "png", "gif", "mp4"]:
                ext = "png"

        return title, f"{title}.{ext}"

    def _get_content_data(self) -> tuple[bytes, str] | None:
        title, _ = self._get_filename()

        if self.content is not None:
            json_data = json.dumps(self.model_dump(), indent=2, default=str)
            content_bytes = json_data.encode('utf-8')
            return content_bytes, 'application/json'

        try:
            response = http_get(self.url)
            if response.status_code != 200:
                logger.error(f"Download rejected {title}: {response.status_code}")
                return None
            return response.content, response.headers.get("content-type", "application/octet-stream")
        except Exception as e:
            logger.error(f"Download failed {title}: {e}")
            return None

    def handle(self, directory: str | None = None, bucket: str | None = None) -> str | None:
        logger.debug(f'Handling reddit post titled "{self.title}" with url {self.url}')

        if directory is not None:
            return self.download(directory)

        if bucket is not None:
            return self.upload(bucket)

        return None

    def download(self, directory: str | None = None) -> bool:
        if directory is None:
            raise ValueError("directory is required")

        _, filename = self._get_filename()
        filepath = os_path.join(directory, filename)

        if os_path.exists(filepath):
            return True

        content_data = self._get_content_data()
        if content_data is None:
            return False

        content_bytes, _ = content_data

        with open(filepath, "wb") as f:
            f.write(content_bytes)

        return True

    def upload(self, bucket: str | None = None) -> bool:
        if bucket is None:
            raise ValueError("bucket is required")

        title, object_name = self._get_filename()

        bucket_parts = bucket.split("/", 1)
        bucket_name = bucket_parts[0]
        prefix = bucket_parts[1] + "/" if len(bucket_parts) > 1 else ""
        full_object_name = prefix + object_name

        content_data = self._get_content_data()
        if content_data is None:
            return False

        content_bytes, content_type = content_data

        try:
            data = BytesIO(content_bytes)
            data.seek(0)
            length = len(content_bytes)

            minio_client.put_object(
                bucket_name=bucket_name,
                object_name=full_object_name,
                data=data,
                length=length,
                content_type=content_type,
            )
            return True
        except Exception as e:
            logger.error(f"Upload failed {title}: {e}")
            return False

