# Poker Training

A terminal program for training your poker intuition. It deals random Texas Hold'em
situations and shows your a priori win probability (Monte Carlo, 1000 samples).

## Requirements

- [uv](https://docs.astral.sh/uv/)
- Python 3.14+ (uv will fetch it if needed)

## Setup

```sh
git clone git@github.com:RobertKihlborg/poker-training.git
cd poker-training
uv sync
```

## Usage

```sh
uv run poker-training
```

1. Choose the number of players (2-10).
2. Choose how many shared cards are revealed (0, 3, 4 or 5).
3. Look at your hand (and the board, if any) and guess your win chance.
4. Press **Enter** to reveal the win probability. An x-way tie counts as 1/x of a win.
5. Press **Enter** again for a new hand. Quit with **Ctrl+C**.

## Tests

```sh
uv run pytest
```

## Layout

- `src/poker_training/evaluator.py` - hand evaluation and Monte Carlo simulation
- `src/poker_training/cli.py` - terminal UI (built with [rich](https://github.com/Textualize/rich))
- `tests/` - unit tests
