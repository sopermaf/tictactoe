"""Game definition for running TicTacToe with AI using MinMax algorithm"""

import itertools
from abc import ABC, abstractmethod

import click


class AbstractPlayer(ABC):
    @abstractmethod
    def decide_turn(self, game) -> int:
        pass


class Game:
    """Board used to play TicTacToe"""

    def __init__(self):
        self.tile = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
        self.turn_count = 1

    def display(self):
        """Displays board"""
        for i in range(3):
            offset = i * 3
            click.echo(
                str(self.tile[offset])
                + " "
                + str(self.tile[offset + 1])
                + " "
                + str(self.tile[offset + 2]),
            )

    def user_turn(self):
        return self.turn_count % 2 != 0

    def turn(self, square: int):
        piece = "x" if self.user_turn() else "o"
        self.tile[square] = piece
        self.turn_count += 1

    def undo_turn(self, square):
        if self.tile[square] == "-":
            click.echo(
                "ERROR UndoTurn: no turn existed in square " + str(square) + " to undo",
            )
            return

        self.tile[square] = "-"
        self.turn_count -= 1

    def squares_free(self) -> list[int]:
        return [i for i, space in enumerate(self.tile) if space == "-"]

    def has_won(self, player) -> bool:
        """Check if tiles match for a player win condition"""
        horizontals = ((i, i + 1, i + 2) for i in range(0, 9, 3))
        verticals = ((i, i + 3, i + 6) for i in range(3))
        diagonals = ((0, 4, 8), (2, 4, 6))

        for row in itertools.chain(horizontals, verticals, diagonals):
            if all(player == self.tile[i] for i in row):
                return True
        return False

    def is_over(self) -> bool:
        for player in ("x", "o"):
            if self.has_won(player):
                click.echo(f"##### {player.upper()!r} wins the game#####")
                return True

        return not bool(self.squares_free())

    def run_game(self, *players: "AbstractPlayer"):
        click.echo("***START GAME***")

        for player in itertools.cycle(players):
            if self.is_over():
                break

            self.display()
            square_to_place = player.decide_turn(self)
            self.turn(square_to_place)

        self.display()
