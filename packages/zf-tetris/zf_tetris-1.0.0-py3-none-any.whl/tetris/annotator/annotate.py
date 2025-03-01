from base64 import b64encode
from collections import OrderedDict
from glob import glob
from json import dump as json_dump
from json import dumps as json_dumps
from json import load as json_load
from json import loads as json_loads
from os import path as os_path
from random import choice as random_choice
from re import search as re_search
from sys import argv

from loguru import logger
from openai import OpenAI
from PIL import Image
from pydantic import BaseModel
from PyQt5.QtWidgets import QApplication

from ..config import settings
from ..models import models
from .icons import Icons
from .image import ImageAnnotationTool

TETRIS_PATH = settings.TETRIS_PATH


class TextZones(BaseModel):
    text_zones: list[models.OpenAITextZone]


class Annotator:
    def __init__(self, templates_dir: str, examples_dir: str):
        if not os_path.exists(templates_dir):
            logger.error(f"Templates directory {templates_dir} does not exist")
            return
        if not os_path.exists(examples_dir):
            logger.error(f"Examples directory {examples_dir} does not exist")
            return

        self.templates_dir = templates_dir
        self.examples_dir = examples_dir

        self.app = None
        self.tool = None
        self.client = OpenAI(api_key=settings.TETRIS_OPENAI_API_KEY)
        self.templates = OrderedDict()

    def run(self, meme, randomize):
        if not self.app:
            self.app = QApplication(argv)
            Icons.load_icons()

        meme_path = self.__select_meme__(meme, randomize)
        if not meme_path:
            logger.error(f"Meme {meme} not found")
            return

        logger.info(f"Picked meme {meme_path} for annotation")
        self.annotate(meme_path)

        self.app.exec_()

    def annotate(self, image_path: str):
        image_source = models.FileSource.from_filepath(image_path)
        description = self.__describe_meme__(image_source=image_source)
        zones = self.__label_meme__(
            image_source=image_source, description=description
        )
        logger.info(f"Zones: {zones}")
        self.preview(image_source, description, zones)

    def preview(
        self,
        image_source: str | models.FileSource,
        image_description: str,
        text_zones: list[models.TextZone],
    ):
        if isinstance(image_source, str):
            image_source = models.FileSource.from_filepath(image_source)

        if self.tool:
            self.tool.close()

        self.tool = ImageAnnotationTool(image_source, image_description, text_zones)
        self.tool.annotationSaved.connect(self.on_saved)
        self.tool.refreshed.connect(self.on_refreshed)
        self.tool.show()

    def process_events(self):
        self.app.processEvents()
        if not self.tool.isVisible():
            self.app.quit()

    def on_saved(self, result: tuple[models.FileSource, list[models.Zone], bool]):
        image_source, zones, description, should_close = result

        self.templates[image_source.name]["description"] = description
        self.templates[image_source.name]["text_zones"] = [
            zone.model_dump() for zone in zones if zone.type == models.ZoneType.TextZone
        ]
        self.templates[image_source.name]["image_zones"] = [
            zone.model_dump()
            for zone in zones
            if zone.type == models.ZoneType.ImageZone
        ]

        with open(f"{image_source.dir}/templates.json", "w") as f:
            json_dump(self.templates, f, indent=2)

        if should_close:
            self.tool.close()

        logger.info("Saved annotations")

    def on_refreshed(self, result):
        meme_path = self.__select_meme__(None, True)
        if meme_path:
            self.annotate(meme_path)
        else:
            logger.error("No memes found for refresh")

    def __select_meme__(self, meme: str, randomize: bool) -> str:
        meme_path, meme_name = None, None

        meme_paths = glob(f"{self.templates_dir}/*.png")
        meme_schemas_paths = glob(f"{self.templates_dir}/*.json")

        # logger.info(f"Meme paths: {meme_paths}")
        # logger.info(f"Meme schemas paths: {meme_schemas_paths}")

        # del all path from meem_paths that end with -1.png or -2.png or -3.png basically -\d.png
        meme_paths = [path for path in meme_paths if not re_search(r"_\d+\.png", path)]

        logger.info(f"Found {len(meme_paths)} meme paths at {self.templates_dir}")

        all_meme_schemas = {}
        for meme_schemas_path in meme_schemas_paths:
            meme_schemas_dict = json_load(
                open(meme_schemas_path, "r")
            )  # directory level

            for k, v in meme_schemas_dict.items():
                p = meme_schemas_path.replace("templates.json", f"{k}.png")
                all_meme_schemas[(p, k)] = v

        logger.info(f"Loaded schemas for {len(all_meme_schemas)} memes")

        if randomize:
            meme_path = random_choice(meme_paths)
            meme_name = os_path.basename(meme_path).replace(".png", "")

            while (meme_path, meme_name) in all_meme_schemas.keys():
                meme_path = random_choice(meme_paths)
                meme_name = os_path.basename(meme_path).replace(".png", "")
        else:
            meme = meme.strip().replace(" ", "_")

            for meme_path in meme_paths:
                if meme in meme_path:
                    meme_path = meme_path
                    break

        return meme_path

    def __describe_meme__(self, image_source: models.FileSource):
        templates_path = f"{image_source.dir}/templates.json"

        if os_path.exists(templates_path):
            with open(templates_path, "r") as f:
                self.templates = OrderedDict(sorted(json_load(f).items()))
        else:
            self.templates = OrderedDict()

        description = ""
        if (
            image_source.name in self.templates
            and "description" in self.templates[image_source.name]
        ):
            description = self.templates[image_source.name]["description"]
        else:
            image_base64 = None
            with open(image_source.path, "rb") as image_file:
                image_base64 = b64encode(image_file.read()).decode("utf-8")
                logger.debug(
                    f"Loaded image {image_source.name} from {image_source.path}"
                )

            result = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in understanding memes and explaining when to use them",
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Explain the meme named {image_source.name} in two sentences. First sentence should describe the meme, second sentence should describe when to use it.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}",
                                },
                            },
                        ],
                    },
                ],
                max_tokens=200,
            )

            name_formats = models.name_formats(image_source.name)
            description = result.choices[0].message.content

            self.templates[image_source.name] = {
                "name": name_formats[models.NameFormat.SPACE_CASE],
                "filename": f"{image_source.name}.{image_source.type}",
                "description": description,
            }

            self.templates = OrderedDict(sorted(self.templates.items()))

        if (
            "width" not in self.templates[image_source.name]
            or "height" not in self.templates[image_source.name]
        ):
            with Image.open(image_source.path) as img:
                width, height = img.size

            self.templates[image_source.name]["width"] = width
            self.templates[image_source.name]["height"] = height

        logger.info(f"Successfully described meme {image_source.name}: {description}")

        return description

    def __label_meme__(
        self, image_source: models.FileSource, description: str
    ) -> list[models.Zone]:
        templates_path = f"{image_source.dir}/templates.json"

        if os_path.exists(templates_path):
            with open(templates_path, "r") as f:
                self.templates = OrderedDict(sorted(json_load(f).items()))
        else:
            self.templates = OrderedDict()

        # list of text and image zones
        zones: list[models.Zone] = []

        if image_source.name in self.templates:
            if "text_zones" in self.templates[image_source.name]:
                text_zones = self.templates[image_source.name]["text_zones"]
                for zone_data in text_zones:
                    if "type" not in zone_data:
                        zone_data["type"] = models.ZoneType.TextZone
                    if "angle" not in zone_data:
                        zone_data["angle"] = 0

                    zone = models.TextZone.model_validate(zone_data)
                    zones.append(zone)

                logger.info(
                    f"Loaded {len(text_zones)} text zones from templates for meme {image_source.name}"
                )

            if "image_zones" in self.templates[image_source.name]:
                image_zones = self.templates[image_source.name]["image_zones"]

                for zone_data in image_zones:
                    if "type" not in zone_data:
                        zone_data["type"] = models.ZoneType.ImageZone
                    if "angle" not in zone_data:
                        zone_data["angle"] = 0

                    zone = models.ImageZone.model_validate(zone_data)
                    zones.append(zone)

                logger.info(
                    f"Loaded {len(image_zones)} image zones from templates for meme {image_source.name}"
                )

            return zones

        # If no zones are not found in templates, proceed with GPT-based labeling
        examples_paths = glob(f"{self.examples_dir}/*.png")
        logger.info(f"Found {len(examples_paths)} examples at {self.examples_dir}")

        examples = []
        for example_path in examples_paths:
            if image_source.name in example_path:
                examples.append(example_path)

        image_base64 = self.__load_base64__(image_source.path)
        examples_base64 = [
            self.__load_base64__(example_path) for example_path in examples
        ]

        text_zones_examples = [
            {
                "bbox": [71, 344, 194, 103],
                "font_family": "Arial",
                "font_size": 24,
                "font_color": "#000000",
                "title": "Dumb Text",
                "description": "This text denotes an opinion believed by people on the lowest end of the intelligence spectrum. They sometimes may believe in a powerful idea without even realizing its true power",
                "examples": ["Brain size doesn't matter", "I only need one monitor"],
            },
            {
                "bbox": [61, 398, 596, 251],
                "font_family": "Arial",
                "font_size": 52,
                "font_color": "#000000",
                "title": "Suspicious Woman Text",
                "description": 'This text "I bet he\'s thinking about other women" usually denotes the thoughts of a women that represent her doubts about her man while they are lying in bed',
                "examples": ["I bet he's thinking about other women"],
            },
        ]

        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert in labeling memes. You are given an image of a meme and a list of 3 examples of using that meme. You goal is to fill the text zones object for the Meme with annotations of what to fill in that text zone. The dimensions of text zones bounding boxes are in pixels. Here are some examples of how the text zones look like: {json_dumps(text_zones_examples)}",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"You are givent the meme named {image_source.name} and its description: {description}. Fill the text zones object for the Meme with annotations of what to fill in that text zone.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}",
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{examples_base64[0]}",
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{examples_base64[1]}",
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{examples_base64[2]}",
                            },
                        },
                    ],
                },
            ],
            response_format=TextZones,
        )

        if not completion.choices:
            logger.error(f"No completion choices returned for meme {image_source.name}")
            return None

        result_msg = completion.choices[0].message
        result_str = ""
        if result_msg.refusal:
            logger.error(f"ChatGPT refused due to {result_msg.refusal}")
        else:
            result_str = result_msg.content

        logger.info(f"Parsed: {result_msg.parsed}")
        logger.info(f"ChatGPT returned: {result_str}")

        result = json_loads(result_str)
        logger.info(f"Result: {result}")

        if "text_zones" not in result:
            logger.error(f"No text zones found in result for meme {image_source.name}")
            return None

        for tz in result["text_zones"]:
            zones.append(
                models.TextZone(
                    type=models.ZoneType.TextZone,
                    bbox=tuple(tz["bbox"]),
                    font_family=tz["font_family"],
                    font_size=tz["font_size"],
                    font_color=tz["font_color"],
                    title=tz["title"],
                    description=tz["description"],
                    examples=tz["examples"],
                )
            )

        # Save the new zones to the templates
        self.templates[image_source.name]["zones"] = [
            zone.model_dump() for zone in zones
        ]
        with open(templates_path, "w") as f:
            json_dump(self.templates, f, indent=2)

        logger.info(f"Successfully labeled meme {image_source.name}: {zones}")
        return zones

    def __load_base64__(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return b64encode(image_file.read()).decode("utf-8")
