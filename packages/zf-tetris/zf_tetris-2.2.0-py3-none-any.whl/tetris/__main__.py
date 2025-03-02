from asyncio import run
from datetime import datetime
from os import makedirs
from os import path as os_path
from sys import stderr, stdout

import click
from loguru import logger

from tetris.trender.reddit import RedditTrender
from tetris.trender.minio import minio_client
from tetris.version import __version__

logger.remove()
logger.add(stdout, level="INFO")
logger.add(stderr, level="WARNING")

def parse_str_list(ctx, param, value) -> list[str]:
    if not value:
        return []
    return value.split(',')


async def async_main(subreddits, limit, span, download, upload):
    async with RedditTrender() as t:
        todays_date = datetime.now().strftime("%Y-%m-%d")

        memes = await t.top_k_posts(subreddits, limit=limit, span=span)

        directory = f"{download}/{todays_date}"
        bucket = f"{upload}/{todays_date}"

        if download:
            ensure_path(directory)

        if upload:
            ensure_bucket(upload)

        for meme in memes:
            if download:
                _ = meme.download(directory)

            if upload:
                _ = meme.upload(bucket)


def ensure_path(path):
    if not os_path.exists(path):
        logger.info(f"Creating directory {path}")
        makedirs(path)

def ensure_bucket(bucket_name):
    try:
        exists = minio_client.bucket_exists(bucket_name)
        if not exists:
            logger.info(f"Creating bucket {bucket_name}")
            minio_client.make_bucket(bucket_name)
    except Exception as e:
        logger.error(f"Error checking/creating bucket: {e}")
        raise

@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.option("--subreddits", type=str, required=True, callback=parse_str_list, help="Subreddits to process")
@click.option("--limit", type=int, default=10)
@click.option("--span", type=str, default="day")
@click.option("--download", type=str, default=None, help="Local directory to save memes")
@click.option("--upload", type=str, default=None, help="Minio bucket name")
def reddit(subreddits, limit, span, download, upload):
    if not subreddits:
        raise click.UsageError("Subreddits are required")

    subreddit_names = []
    for subreddit in subreddits:
        subreddit = subreddit.strip()
        if not subreddit:
            continue

        subreddit = subreddit.split("/")[-1]
        subreddit_names.append(subreddit)

    if download is None and upload is None:
        raise click.UsageError("Either download path or upload bucket name must be provided")

    run(async_main(subreddit_names, limit, span, download, upload))


if __name__ == "__main__":
    cli()
