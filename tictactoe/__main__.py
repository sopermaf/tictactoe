"""Command-line interface."""

import logging
import random

import click

from .game import TicTacToeBoard
from .player.ai import MaxMinAI
from .player.human import TerminalUser


@click.command()
@click.version_option()
def main() -> None:
    """Tictactoe   Maxmin."""
    players = [TerminalUser("x"), MaxMinAI("o")]
    random.shuffle(players)

    board = TicTacToeBoard()
    board.game_loop(*players)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(prog_name="tictactoe")  # pragma: no cover
