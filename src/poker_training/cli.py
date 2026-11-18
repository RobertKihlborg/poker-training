"""Terminal UI for the poker training program (basic mode)."""

import random
import sys

from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import IntPrompt
from rich.text import Text

from .evaluator import card_str, win_probability

console = Console()
SAMPLES = 1000
BOARD_SIZES = (0, 3, 4, 5)


def render_card(card: int | None) -> Panel:
    if card is None:
        return Panel(Text("?", justify="center"), width=7, height=5, style="dim")
    s = card_str(card)
    color = "red" if card // 13 in (1, 2) else "white"
    return Panel(
        Align.center(Text(s, style=f"bold {color}"), vertical="middle"),
        width=7,
        height=5,
    )


def render_cards(title: str, cards: list[int]) -> Panel:
    from rich.columns import Columns

    body = Columns([render_card(c) for c in cards], padding=(0, 0)) if cards else Text("(none)", style="dim")
    return Panel(body, title=title, border_style="cyan", expand=False)


def setup() -> tuple[int, int]:
    console.print(Panel("[bold]Poker Training[/bold]", style="green"))
    players = IntPrompt.ask("Number of players", choices=[str(n) for n in range(2, 11)], default=2, console=console)
    board = IntPrompt.ask(
        "Shared cards revealed", choices=[str(n) for n in BOARD_SIZES], default=3, console=console
    )
    return players, board


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        players, board_size = setup()
        while True:
            deck = random.sample(range(52), 2 + board_size)
            hero, board = deck[:2], deck[2:]
            console.clear()
            console.print(f"[dim]{players} players · {board_size} shared cards · Ctrl+C to quit[/dim]")
            if board:
                console.print(render_cards("Board", board))
            console.print(render_cards("Your hand", hero))
            console.input("[dim]Press Enter to reveal win probability…[/dim]")
            with console.status("Simulating…"):
                p = win_probability(hero, board, players, SAMPLES)
            console.print(Group(Text(f"Win probability: {p * 100:.1f}%", style="bold green")))
            console.input("[dim]Press Enter for next hand…[/dim]")
    except (KeyboardInterrupt, EOFError):
        console.print("\nBye!")
