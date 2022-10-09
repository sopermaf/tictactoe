"""Command-line interface."""
import click

from .game import Game
from .player import AI, TerminalUser


@click.command()
@click.version_option()
def main() -> None:
    """Tictactoe   Maxmin."""
    game = Game()
    game.run_game(AI("o"), TerminalUser())


if __name__ == "__main__":
    main(prog_name="TicTacToe")  # pragma: no cover
