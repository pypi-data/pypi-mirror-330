from datetime import datetime
from asyncpraw import Reddit
from loguru import logger

from tetris.trender.config import settings
from tetris.trender import models

REDDIT_CLIENT_ID = settings.TETRIS_REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET = settings.TETRIS_REDDIT_CLIENT_SECRET

class RedditTrender:
    def __init__(self):
        self.reddit_client = Reddit(
            client_id=settings.TETRIS_REDDIT_CLIENT_ID,
            client_secret=settings.TETRIS_REDDIT_CLIENT_SECRET,
            user_agent="Memician/1.0",
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.reddit_client.close()

    async def top_k_posts(self, subreddits: list[str], limit: int = 10, span: str = "day"):
        logger.info(f"Processing {len(subreddits)} subreddits")

        for subreddit in subreddits:
            subreddit = await self.reddit_client.subreddit(subreddit)

            results: list[models.RedditPost] = []
            async for submission in subreddit.top(span, limit=limit):
                try:
                    results.append(
                        models.RedditPost(
                            id=submission.id,
                            subreddit=submission.subreddit.display_name,
                            creator=submission.author.name,
                            title=submission.title,
                            url=submission.url,
                            permalink=submission.permalink,
                            num_likes=submission.ups,
                            num_comments=submission.num_comments,
                            num_shares=submission.num_crossposts,
                            ratio_likes=submission.upvote_ratio,
                            created_at=datetime.fromtimestamp(submission.created_utc),
                        )
                    )
                except Exception as e:
                    logger.error(f"failed to parse submission: {e}")
            return results