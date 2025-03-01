import os

import requests
from bs4 import BeautifulSoup
from loguru import logger
from tqdm import tqdm

MEMICIAN_PATH = os.getenv("MEMICIAN_PATH")


class Scraper:
    def __init__(self):
        self.domain = "imgflip.com"
        self.filters = {
            "meme": "h3.mt-title > a",
            "template": "a.meme-link > img",
            "example": ".base-img",
        }
        self.scraped = set()

    def scrape_index(self, index_url: str, output_dir: str, limit: int = 3):
        response = requests.get(index_url)
        soup = BeautifulSoup(
            response.content,
            "html.parser",
        )

        meme_elems = soup.select(self.filters["meme"])

        meme_urls: list[str] = []
        for e in meme_elems:
            if "href" in e.attrs:
                meme_url = self.__make_url__(e["href"])
                meme_urls.append(meme_url)

        logger.debug(f"Found {len(meme_urls)} memes")

        for meme_url in meme_urls:
            self.scrape_meme(meme_url, output_dir, limit)

    def scrape_meme(self, meme_url: str, output_dir: str, limit: int = 3):
        meme_name = meme_url.split("/")[-1]

        response = requests.get(meme_url)
        soup = BeautifulSoup(
            response.content,
            "html.parser",
        )

        # scrape template
        template_elem = soup.select_one(self.filters["template"])
        if not template_elem:
            logger.error("Did not find template url")
            return

        template_url = self.__make_url__(template_elem["src"])
        template_ext = template_url.split(".")[-1]

        template_path = os.path.join(output_dir, f"{meme_name.lower()}.{template_ext}")

        self.download(url=template_url, path=template_path)

        # scrape examples
        example_elems = soup.select(self.filters["example"])

        example_urls = []
        for e in example_elems:
            if "src" in e.attrs:
                example_urls.append(self.__make_url__(e["src"]))

        limit = min(limit, len(example_urls))

        logger.info(f"Downloading {limit} examples for {meme_name}")

        for i, example_url in tqdm(enumerate(example_urls), total=limit):
            if i >= limit:
                break

            example_path = os.path.join(output_dir, f"{meme_name.lower()}-{i}.jpg")
            self.download(url=example_url, path=example_path)

    def download(self, url: str, path: str):
        path = path.replace("-", "_")

        if (url, path) in self.scraped or os.path.exists(path):
            logger.debug(f"Skipping {url} because it has was already scraped")
            return False

        response = requests.get(url)

        if response.status_code == 200:
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, "wb") as file:
                file.write(response.content)

            self.scraped.add((url, path))
            logger.debug(f"Downloaded {url} to {path}")
            return True
        else:
            logger.error(f"Failed to download {url}")

        return False

    def __make_url__(self, partial: str):
        if partial.startswith("//"):
            partial = f"https:{partial}"
        elif partial.startswith("/"):
            partial = f"https://{self.domain}{partial}"
        return partial
