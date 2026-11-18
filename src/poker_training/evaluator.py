"""Hand evaluation and Monte Carlo win probability.

Cards are ints 0..51: rank = card % 13 (0 = deuce ... 12 = ace), suit = card // 13.
"""

import random
from collections import Counter

RANKS = "23456789TJQKA"
SUITS = "♠♥♦♣"


def card_str(card: int) -> str:
    rank = "10" if card % 13 == 8 else RANKS[card % 13]
    return rank + SUITS[card // 13]


def _straight_high(rank_set: set[int]) -> int:
    """Highest card of a straight in rank_set, or -1."""
    for high in range(12, 3, -1):
        if all((high - i) in rank_set for i in range(5)):
            return high
    if {12, 0, 1, 2, 3} <= rank_set:  # wheel
        return 3
    return -1


def evaluate(cards: list[int]) -> tuple:
    """Score the best 5-card hand from 5-7 cards. Higher tuples win."""
    by_suit: dict[int, list[int]] = {}
    for c in cards:
        by_suit.setdefault(c // 13, []).append(c % 13)

    for ranks in by_suit.values():
        if len(ranks) >= 5:
            sf = _straight_high(set(ranks))
            if sf >= 0:
                return (8, sf)
            return (5, *sorted(ranks, reverse=True)[:5])

    counts = Counter(c % 13 for c in cards)
    # groups sorted by (count, rank) descending
    groups = sorted(counts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    top_count = groups[0][1]

    if top_count == 4:
        kicker = max(r for r, _ in groups[1:])
        return (7, groups[0][0], kicker)
    if top_count == 3 and len(groups) > 1 and groups[1][1] >= 2:
        return (6, groups[0][0], groups[1][0])
    st = _straight_high(set(counts))
    if st >= 0:
        return (4, st)
    if top_count == 3:
        kick = sorted((r for r, _ in groups[1:]), reverse=True)[:2]
        return (3, groups[0][0], *kick)
    if top_count == 2:
        pairs = [r for r, n in groups if n == 2]
        if len(pairs) >= 2:
            p1, p2 = pairs[0], pairs[1]
            kicker = max(r for r in counts if r != p1 and r != p2)
            return (2, p1, p2, kicker)
        kick = sorted((r for r, _ in groups[1:]), reverse=True)[:3]
        return (1, groups[0][0], *kick)
    return (0, *sorted(counts, reverse=True)[:5])


def win_probability(
    hero: list[int],
    board: list[int],
    num_players: int,
    samples: int = 1000,
    rng: random.Random | None = None,
) -> float:
    """Hero's equity in [0, 1]; an x-way tie counts as 1/x of a win."""
    rng = rng or random
    known = set(hero) | set(board)
    deck = [c for c in range(52) if c not in known]
    need_board = 5 - len(board)
    need = need_board + 2 * (num_players - 1)
    total = 0.0
    for _ in range(samples):
        drawn = rng.sample(deck, need)
        full_board = board + drawn[:need_board]
        hero_score = evaluate(hero + full_board)
        ties = 1
        lost = False
        for p in range(num_players - 1):
            i = need_board + 2 * p
            score = evaluate(drawn[i : i + 2] + full_board)
            if score > hero_score:
                lost = True
                break
            if score == hero_score:
                ties += 1
        if not lost:
            total += 1 / ties
    return total / samples
