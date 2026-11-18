import random

from poker_training.evaluator import evaluate, win_probability

R = "23456789TJQKA"


def c(s: str) -> int:
    return R.index(s[0]) + 13 * "shdc".index(s[1])


def h(*s: str) -> list[int]:
    return [c(x) for x in s]


def test_category_order():
    hands = [
        h("As", "Kd", "9c", "7h", "5s", "3d", "2c"),  # high card
        h("As", "Ad", "9c", "7h", "5s", "3d", "2c"),  # pair
        h("As", "Ad", "9c", "9h", "5s", "3d", "2c"),  # two pair
        h("As", "Ad", "Ac", "7h", "5s", "3d", "2c"),  # trips
        h("5s", "4d", "3c", "2h", "As", "Kd", "Qc"),  # wheel straight
        h("As", "Ks", "9s", "7s", "5s", "3d", "2c"),  # flush
        h("As", "Ad", "Ac", "7h", "7s", "3d", "2c"),  # full house
        h("As", "Ad", "Ac", "Ah", "5s", "3d", "2c"),  # quads
        h("5s", "4s", "3s", "2s", "As", "Kd", "Qc"),  # straight flush
    ]
    scores = [evaluate(x) for x in hands]
    assert scores == sorted(scores) and len(set(scores)) == len(scores)


def test_kickers_and_ties():
    assert evaluate(h("As", "Kd", "Qc", "Jh", "9s", "3d", "2c")) > evaluate(h("As", "Kd", "Qc", "Jh", "8s", "3d", "2c"))
    assert evaluate(h("As", "Ad", "Kc", "Kh", "9s", "3d", "2c")) == evaluate(h("Ac", "Ah", "Ks", "Kd", "9d", "3s", "2h"))


def test_win_probability_sanity():
    rng = random.Random(1)
    aa = win_probability(h("As", "Ac"), [], 2, 4000, rng)
    assert 0.80 < aa < 0.88  # ~85%
    # royal flush on board is a guaranteed split, so equity is 1/players
    p = win_probability(h("2c", "3d"), h("As", "Ks", "Qs", "Js", "Ts"), 3, 200, rng)
    assert abs(p - 1 / 3) < 1e-9
