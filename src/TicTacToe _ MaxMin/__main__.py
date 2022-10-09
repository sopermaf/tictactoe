"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Tictactoe   Maxmin."""


if __name__ == "__main__":
    main(prog_name="TicTacToe - MaxMin")  # pragma: no cover
