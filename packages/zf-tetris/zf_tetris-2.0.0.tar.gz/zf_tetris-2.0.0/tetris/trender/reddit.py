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

    def _get_url_from_permalink(self, permalink: str) -> str:
        return f"https://www.reddit.com{permalink}"

    async def _get_comments(self, submission, max_comments: int = 10) -> list[models.RedditPost]:
        comments = []

        try:
            await submission.load()
            submission.comment_sort = "top"
            await submission.comments.replace_more(limit=0)

            count = 0
            for comment in submission.comments:
                if count >= max_comments:
                    break

                try:
                    if hasattr(comment, "body") and comment.body and hasattr(comment, "author") and comment.author:
                        comments.append(
                            models.RedditPost(
                                id=comment.id,
                                subreddit=submission.subreddit.display_name,
                                creator=comment.author.name,
                                title=None,
                                content=comment.body,
                                comments=None,
                                url=self._get_url_from_permalink(comment.permalink),
                                permalink=comment.permalink,
                                num_likes=comment.score,
                                num_comments=None,
                                num_shares=None,
                                ratio_likes=None,
                                created_at=datetime.fromtimestamp(comment.created_utc),
                            )
                        )
                        count += 1
                except Exception as e:
                    logger.error(f"Failed to parse comment: {e}")
                    continue

        except Exception as e:
            logger.error(f"Failed to fetch comments: {e}")

        return comments

    async def top_k_posts(self, subreddits: list[str], limit: int = 10, span: str = "day", max_comments: int = 10):
        logger.info(f"Processing {len(subreddits)} subreddits")

        all_results: list[models.RedditPost] = []

        for subreddit in subreddits:
            subreddit = await self.reddit_client.subreddit(subreddit)

            logger.info(f"Fetching top {limit} posts from r/{subreddit.display_name}")

            subreddit_results: list[models.RedditPost] = []
            async for submission in subreddit.top(span, limit=limit):
                try:
                    text_content = submission.selftext if hasattr(submission, 'selftext') else None
                    comments = await self._get_comments(submission, max_comments)

                    subreddit_results.append(
                        models.RedditPost(
                            id=submission.id,
                            subreddit=submission.subreddit.display_name,
                            creator=submission.author.name,
                            title=submission.title,
                            content=text_content,
                            url=submission.url,
                            permalink=submission.permalink,
                            num_likes=submission.ups,
                            num_comments=submission.num_comments,
                            num_shares=submission.num_crossposts,
                            ratio_likes=submission.upvote_ratio,
                            created_at=datetime.fromtimestamp(submission.created_utc),
                            comments=comments
                        )
                    )
                except Exception as e:
                    logger.error(f"failed to parse submission: {e}")

            logger.info(f"Collected {len(subreddit_results)} posts from r/{subreddit.display_name}")
            all_results.extend(subreddit_results)

        logger.info(f"Total posts collected: {len(all_results)}")
        return all_results