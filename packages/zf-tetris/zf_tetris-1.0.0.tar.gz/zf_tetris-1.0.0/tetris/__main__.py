from asyncio import run
from datetime import datetime
from os import makedirs
from os import path as os_path
from sys import stderr, stdout

import click
from loguru import logger

from tetris.annotator.annotate import Annotator
from tetris.config import settings
from tetris.scraper.scraper import Scraper
from tetris.trender.reddit import RedditTrender
from tetris.version import __version__

logger.remove()
logger.add(stdout, level="INFO")
logger.add(stderr, level="WARNING")


async def async_main(subreddits, limit, span):
    async with RedditTrender() as t:
        memes = await t.top_k_posts(subreddits, limit=limit, span=span)

        todays_date = datetime.now().strftime("%Y-%m-%d")
        memes_dir = f"{settings.TETRIS_PATH}/output/memes/{todays_date}"

        if not os_path.exists(memes_dir):
            logger.info(f"Creating directory {memes_dir}")
            makedirs(memes_dir)

        for meme in memes:
            _ = meme.download(memes_dir)


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.option("--subreddits", type=str, multiple=True, default=["memes", "dankmemes"])
@click.option("--limit", type=int, default=10)
@click.option("--span", type=str, default="day")
def download(subreddits, limit, span):
    run(async_main(subreddits, limit, span))


@cli.command()
@click.option("--dir", required=True, help="Directory to save scraped images")
@click.option("--limit", default=3, type=int, help="Number of example images to scrape")
@click.argument("url")
def scrape(dir, limit, url):
    if not url:
        logger.error("Please provide a url")
        return

    scraper = Scraper()

    try:
        dir_path = f"{settings.TETRIS_PATH}/templates/{dir}"

        scrape_fn = scraper.scrape_index if "memetemplates" in url else scraper.scrape_meme

        scrape_fn(url, dir_path, limit)

        logger.info(f"Successfully scraped {len(scraper.scraped)} memes")
    except Exception as e:
        logger.error(f"Error scraping memes: {str(e)}")


@cli.command()
@click.option("--templates", help="Directory containing templates")
@click.option("--examples", help="Directory containing examples")
@click.option("--meme", help="Name of the meme to annotate")
@click.option("--randomize", is_flag=True, help="Randomly pick a meme")
def annotate(templates, examples, meme, randomize):
    if not templates:
        logger.error("Please provide a templates directory")
        return

    if not examples:
        logger.error("Please provide an examples directory")
        return

    if not randomize and not meme:
        logger.error("Either provide a meme or use the --randomize flag")
        return

    annotator = Annotator(templates, examples)
    annotator.run(meme, randomize)


if __name__ == "__main__":
    cli()
