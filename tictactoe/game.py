import abc
import itertools
import logging

import click


class IllegalMoveError(ValueError):
    """Base class for moves that cannot occur"""


class InvalidBoardError(ValueError):
    """Invalid game"""


log = logging.getLogger(__name__)


class AbstractPlayer(abc.ABC):
    def __init__(self, token: str) -> None:
        self.token = token

    @abc.abstractmethod
    def tile_to_play(self, board_state: "TicTacToeBoard") -> int:
        """Select a tile to play"""

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.token == other
        if isinstance(other, AbstractPlayer):
            return self.token == other.token
        raise NotImplementedError


class TicTacToeBoard:
    """Represents the board for the game"""

    EMPTY_SPACE_CHAR = "-"
    _NUM_PLAYERS_REQUIRED = 2
    _NUM_SQUARES = 9

    def __init__(self, initial_board: list[str] | None = None):
        if initial_board:
            if len(initial_board) != self._NUM_SQUARES:
                raise InvalidBoardError(initial_board)
            self._tiles: list[str] = list(initial_board)
        else:
            self._tiles = [self.EMPTY_SPACE_CHAR] * self._NUM_SQUARES
        self.winner: str | None = None

    @property
    def tiles(self) -> list[str]:
        return list(self._tiles)

    def game_loop(self, *players: AbstractPlayer) -> None:
        """main entrypoint for running the game until end"""
        click.echo("***START GAME***")
        for player in itertools.cycle(players):
            self.display_board()
            if self.is_finished:
                break
            chosen_tile_index = player.tile_to_play(self)
            self.apply_turn(player.token, chosen_tile_index)

        click.echo("*** GAME OVER ***")
        if self.winner:
            click.echo(f"*** {self.winner} wins! ***")

    def display_board(self) -> None:
        for i in range(3):
            offset = i * 3
            click.echo(" ".join([self._tiles[offset + j] for j in range(3)]))

    def apply_turn(self, player: str, chosen_tile_index: int) -> None:
        """Updates tiles or raises Exception"""
        # prompt the player to choose a tile and make the move
        if self._tiles[chosen_tile_index] != self.EMPTY_SPACE_CHAR:
            raise IllegalMoveError(chosen_tile_index, self._tiles)
        self._tiles[chosen_tile_index] = player

        # check for a win scenario
        horizontals = ((i, i + 1, i + 2) for i in range(0, 9, 3))
        verticals = ((i, i + 3, i + 6) for i in range(3))
        diagonals = ((0, 4, 8), (2, 4, 6))
        if any(
            all(player == self._tiles[i] for i in row)
            for row in itertools.chain(horizontals, verticals, diagonals)
        ):
            self.winner = player

    @property
    def is_finished(self) -> bool:
        return self.winner is not None or all(
            t != self.EMPTY_SPACE_CHAR for t in self._tiles
        )

    @property
    def free_tiles(self) -> list[int]:
        return [i for i, t in enumerate(self._tiles) if t == self.EMPTY_SPACE_CHAR]
