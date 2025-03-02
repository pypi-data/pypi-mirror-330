# Tetris

<p align="center">
  <img src="https://zf-static.s3.us-west-1.amazonaws.com/tetris-logo128.png" alt="Tetris"/>
</p>

Tetris is a tool for identifying latest trends from news and social media to assist in marketing.

## Installation

```bash
git clone https://github.com/muqsitnawaz/tetris.git
cd tetris
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

You can download memes from Reddit using the `reddit` command. The tool supports both local downloads and uploads to MinIO storage.

### Basic Usage

```bash
python -m tetris reddit --subreddits memes dankmemes
```

### Advanced Options

- `--subreddits`: Specify one or more subreddits (default: None)
- `--limit`: Number of top posts to fetch (default: 10 per subreddit)
- `--span`: Time span for top posts (default: day)
- `--download`: Local directory to save memes (default: None)
- `--upload`: S3 bucket name for uploading (default: None)

### Examples

Download memes to a custom directory:
```bash
python -m tetris reddit --subreddits "memes,dankmemes" --limit 20 --download custom/path/memes
```

Upload memes to a specific MinIO bucket:
```bash
python -m tetris reddit --subreddits "memes,dankmemes" --limit 20 --upload custom-bucket
```

Both download and upload:
```bash
python -m tetris reddit --subreddits "memes,dankmemes" --limit 20 --download local/memes --upload memes-bucket
```

## License

All rights reserved (c) 2024 Zeff Muks