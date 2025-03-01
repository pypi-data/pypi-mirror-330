# Tetris

<p align="center">
  <img src="https://zf-static.s3.us-west-1.amazonaws.com/tetris-logo128.png" alt="Tetris"/>
</p>

Tetris is a tool for identifying latest trends from news and social media to assit in marketing.

## Todo

- [ ] Support for fetching Twitter trends

## Installation

```bash
git clone https://github.com/muqsitnawaz/tetris.git
cd tetris
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

- All memes are located inside the `tetris/library/templates` directory

You can use annotate command with `--randomize` to annotate a randomly selected meme.

```bash
python -m tetris annotate --randomize
```

You can look at exampels of how to the meme is used in the `templates` directory.

Based on the example and the description output by ChatGPT, please annotate it.

<p align="center">
  <img src="https://zf-static.s3.us-west-1.amazonaws.com/tetris-example.gif" alt="Annotation Example"/>
</p>

## License

All rights reserved (c) 2024 Zeff Muks