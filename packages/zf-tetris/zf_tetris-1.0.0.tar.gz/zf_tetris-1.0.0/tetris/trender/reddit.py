from datetime import datetime
from os import path as os_path

from asyncpraw import Reddit
from loguru import logger
from PIL import Image, ImageDraw
# from transformers import LayoutLMv2Processor
# from ultralytics import YOLO

from ..config import settings
from ..models import models

TETRIS_PATH = settings.TETRIS_PATH
REDDIT_CLIENT_ID = settings.TETRIS_REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET = settings.TETRIS_REDDIT_CLIENT_SECRET

# TODO: Automate the capability to auto generate templates from memes


class RedditTrender:
    def __init__(self):
        self.reddit = Reddit(
            client_id=settings.TETRIS_REDDIT_CLIENT_ID,
            client_secret=settings.TETRIS_REDDIT_CLIENT_SECRET,
            user_agent="Memician/1.0",
        )
        # self.text_detection_model = YOLO(
        #     os_path.join(TETRIS_PATH, "tetris/yolov8s.pt"),
        # )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.reddit.close()

    async def top_k_posts(self, subreddits: list[str], limit: int = 10, span: str = "day"):
        logger.info(f"Processing {len(subreddits)} subreddits")

        for subreddit in subreddits:
            subreddit = await self.reddit.subreddit(subreddit)

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

    # def detect_bbox_layout_lmv2(self, image_path):
    #     processor = LayoutLMv2Processor.from_pretrained("microsoft/layoutlmv2-base-uncased")
    #     image = Image.open(image_path).convert("RGB")
    #     encoding = processor(image, return_tensors="pt")
    #     logger.info(f"Encoding: {encoding}")
    #     return encoding["bbox"]

    def detect_bbox_yolov8(self, image_path):
        image = Image.open(image_path)
        results = self.text_detection_model(image)
        # for result in results:
        #     logger.debug(result.boxes)
        bounding_boxes = results[0].boxes.xyxy.cpu().numpy()
        return bounding_boxes

    def merge_bounding_boxes(self, boxes, threshold=8):
        merged = []
        boxes = sorted(boxes, key=lambda x: x[0])  # Sort by x1

        while boxes:
            current = boxes.pop(0)

            while boxes and self.should_merge(current, boxes[0], threshold):
                next_box = boxes.pop(0)
                current = self.merge_boxes(current, next_box)

            merged.append(current)

        return merged

    def should_merge(self, box1, box2, threshold):
        return (box2[0] - box1[2] <= threshold) or (box2[1] - box1[3] <= threshold)

    def merge_boxes(self, box1, box2):
        return [min(box1[0], box2[0]), min(box1[1], box2[1]), max(box1[2], box2[2]), max(box1[3], box2[3])]

    def visualize_bounding_boxes(self, image_path, bounding_boxes, merged=False):
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

        width, height = image.size

        if not merged:
            bounding_boxes = self.merge_bounding_boxes(bounding_boxes[0].tolist())

        for i, box in enumerate(bounding_boxes):
            if box == [1000, 1000, 1000, 1000]:
                continue
            x1, y1, x2, y2 = box
            x1, y1, x2, y2 = (
                int(x1 * width / 1000),
                int(y1 * height / 1000),
                int(x2 * width / 1000),
                int(y2 * height / 1000),
            )
            color = colors[i % len(colors)]
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

        output_path = f"{os_path.splitext(image_path)[0]}_with_merged_boxes.png"
        image.save(output_path)
        return output_path
