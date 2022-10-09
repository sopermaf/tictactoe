"""Command-line interface."""
import click

from . import game

@click.command()
@click.version_option()
def main() -> None:
    """Tictactoe   Maxmin."""
    game.game_loop()


if __name__ == "__main__":
    main(prog_name="TicTacToe - MaxMin")  # pragma: no cover
