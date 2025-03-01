import tweepy
from loguru import logger
from ..config import settings
from ..models import models

class TwitterTrender:
    def __init__(self):
        self.client = tweepy.Client(bearer_token=settings.TETRIS_TWITTER_BEARER_TOKEN)

    def get_trending_topics(self, woeid=1, limit=10):
        try:
            trends = self.client.trends_place(woeid)
            return [
                models.TrendingTopic(
                    name=trend['name'],
                    description=trend.get('tweet_volume', 'N/A'),
                    volume=trend.get('tweet_volume')
                )
                for trend in trends[0][:limit]
            ]
        except Exception as e:
            logger.error(f"Error fetching trending topics: {e}")
            return []

    def get_sample_tweets(self, query, limit=10):
        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                tweet_fields=['public_metrics', 'created_at', 'author_id'],
                expansions=['attachments.media_keys', 'author_id'],
                media_fields=['url', 'preview_image_url'],
                user_fields=['username'],
                max_results=limit
            )

            results = []
            for tweet in tweets.data:
                media = next((m for m in tweets.includes['media'] if m.media_key == tweet.attachments['media_keys'][0]), None) if tweet.attachments else None
                author = next((u for u in tweets.includes['users'] if u.id == tweet.author_id), None)
                if author:
                    result = models.TwitterPost(
                        id=str(tweet.id),
                        username=author.username,
                        text=tweet.text,
                        likes=tweet.public_metrics['like_count'],
                        retweets=tweet.public_metrics['retweet_count'],
                        created_at=tweet.created_at,
                        image_url=media.url or media.preview_image_url if media else None
                    )
                    results.append(result)

            return results

        except Exception as e:
            logger.error(f"Error fetching sample tweets: {e}")
            return []

def run(woeid=1, topic_limit=10, tweet_limit=10):
    trender = TwitterTrender()
    trending_topics = trender.get_trending_topics(woeid, topic_limit)

    for topic in trending_topics:
        logger.info(f"Trending Topic: {topic.name}")
        logger.info(f"Description: {topic.description}")
        logger.info(f"Volume: {topic.volume}")
        logger.info("Sample Tweets:")

        sample_tweets = trender.get_sample_tweets(topic.name, tweet_limit)
        for tweet in sample_tweets:
            logger.info(f"  Tweet: https://twitter.com/{tweet.username}/status/{tweet.id}")
            logger.info(f"  Username: {tweet.username}")
            logger.info(f"  Text: {tweet.text}")
            logger.info(f"  Likes: {tweet.likes}")
            logger.info(f"  Retweets: {tweet.retweets}")
            logger.info(f"  Created at: {tweet.created_at}")
            logger.info(f"  Image URL: {tweet.image_url}")
            logger.info("  ---")

        logger.info("===")

    return trending_topics

if __name__ == "__main__":
    run(woeid=1, topic_limit=5, tweet_limit=3)