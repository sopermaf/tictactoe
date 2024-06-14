import click

from tictactoe.game import AbstractPlayer, TicTacToeBoard


class TerminalUser(AbstractPlayer):
    def tile_to_play(self, board: TicTacToeBoard) -> int:
        while True:
            try:
                turn: int = int(input("Enter turn (0-8): "))
            except ValueError:
                click.echo("invalid selection", err=True, color=True)
            else:
                if turn in board.free_tiles:
                    break
                click.echo("tile is not free")
                board.display_board()
        return turn
