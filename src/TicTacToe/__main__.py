"""Command-line interface."""
import click

from TicTacToe.player import AI, TerminalUser

from . import game


@click.command()
@click.version_option()
def main() -> None:
    """Tictactoe   Maxmin."""
    game.Game.run_game(AI("o"), TerminalUser())


if __name__ == "__main__":
    main(prog_name="TicTacToe")  # pragma: no cover
