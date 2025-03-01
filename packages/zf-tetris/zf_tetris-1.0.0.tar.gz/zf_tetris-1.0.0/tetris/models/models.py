from datetime import datetime
from enum import Enum
from os import path as os_path
from re import findall

from loguru import logger
from pydantic import BaseModel, Field
from requests import get as http_get


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

    def download(self, directory: str | None = None) -> str | None:
        if directory is None:
            raise ValueError("directory is required")

        title = self.title.strip().lower().replace(" ", "_")

        ext = self.url.split(".")[-1]
        if ext not in ["jpg", "jpeg", "png", "gif"]:
            ext = "png"

        filename = f"{title}.{ext}"
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


class TrendingTopic(BaseModel):
    name: str
    description: str
    volume: int | None


class TwitterPost(BaseModel):
    id: str
    username: str
    text: str
    likes: int
    retweets: int
    created_at: datetime
    image_url: str | None


class NameFormat(Enum):
    CAMEL_CASE = "CAMEL_CASE"  # NameFormat
    SNAKE_CASE = "SNAKE_CASE"  # name_format
    SPACE_CASE = "SPACE_CASE"  # Name Format


def name_formats(s: str) -> dict[NameFormat, str]:
    def split_camel_case(s):
        return findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z][a-z]|\d|\W|$)|\d*)", s)

    if "_" in s:
        words = s.lower().split("_")
    elif " " in s:
        words = s.lower().split()
    else:
        words = [word.lower() for word in split_camel_case(s)]

    return {
        NameFormat.CAMEL_CASE: "".join(word.capitalize() for word in words),
        NameFormat.SNAKE_CASE: "_".join(words),
        NameFormat.SPACE_CASE: " ".join(word.capitalize() for word in words),
    }


class FileSource(BaseModel):
    name: str = Field(..., description="The name of the file")
    type: str = Field(..., description="The type of the file")
    dir: str = Field(..., description="The directory of the file")
    path: str = Field(..., description="The full path of the file")

    @classmethod
    def from_filepath(cls, filepath: str) -> "FileSource":
        dir = os_path.dirname(filepath)  # YYYY-MM-DD
        path = os_path.abspath(filepath)  # /path/to/templates/YYYY-MM-DD/flex_tape.png
        name = os_path.basename(path).split(".")[0]  # flex_tape
        file_type = os_path.splitext(path)[1].lstrip(".")  # png
        return cls(name=name, type=file_type, dir=dir, path=path)

    def beautify_name(self) -> str:
        return name_formats(self.name)[NameFormat.SPACE_CASE]

    class Config:
        arbitrary_types_allowed = True


class OpenAITextZone(BaseModel):
    bbox: list[int]
    font_family: str
    font_size: int
    font_color: str
    title: str
    description: str
    examples: list[str]


class ZoneType(str, Enum):
    TextZone = "TextZone"
    ImageZone = "ImageZone"

    def short_name(self) -> str:
        return "TZ" if self == ZoneType.TextZone else "IZ"


class Zone(BaseModel):
    type: ZoneType
    bbox: tuple[int, int, int, int]
    title: str
    description: str
    examples: list[str]
    angle: float

    @property
    def pos(self) -> tuple[int, int]:
        return self.bbox[0], self.bbox[1]

    @property
    def dimensions(self) -> tuple[int, int]:
        return self.bbox[2], self.bbox[3]

    def __mul__(self, other: float) -> "Zone":
        bbox = tuple(int(coord * other) for coord in self.bbox)
        return self.__class__(
            type=self.type,
            bbox=bbox,
            title=self.title,
            description=self.description,
            examples=self.examples.copy(),
            angle=self.angle,
            **self.extra_attributes(),
        )

    def __truediv__(self, other: float) -> "Zone":
        return self * (1.0 / other)

    def extra_attributes(self) -> dict:
        return {}

    class Config:
        use_enum_values = True


class TextZone(Zone):
    font_family: str
    font_size: int
    font_color: str

    def extra_attributes(self) -> dict:
        return {
            "font_family": self.font_family,
            "font_size": self.font_size,
            "font_color": self.font_color,
        }


class ImageZone(Zone):
    def extra_attributes(self) -> dict:
        return {}
