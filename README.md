# The World in One Day — 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/masboyganteng/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/masboyganteng/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up the world's news of **Wednesday 18 November 2026**,
drawn as a newspaper front page: masthead + date, a hero panel for the
U.S.–Iran escalation in the Gulf of Oman, six secondary stories (Kerch
Bridge, Gaza, COP31, Peltola's Alaska win, Pattinson as Bond, the An-12
crash), and an "Also today" strip.

## How it works

- `draw.py` renders `entry.png` (1024×1024, flat-design infographic) with
  Pillow. Every letter and shape is drawn by code — no AI-generated image,
  no external asset.
- `main.py` (Python 3.13, standard library only, no network) copies
  `entry.png` to `/output/entry.png`. Running it twice writes identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The image lands at `out/entry.png`.
