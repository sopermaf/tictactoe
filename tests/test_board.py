"""Test cases for the __main__ module."""

import pytest

from tictactoe.game import AbstractPlayer, TicTacToeBoard


class BasicPlayer(AbstractPlayer):
    """Follows given moves from init"""

    def __init__(self, token, *moves) -> None:
        self.moves = iter(moves)
        super().__init__(token)

    def tile_to_play(self, game) -> int:
        return next(self.moves)


class Dummy(AbstractPlayer):
    """Test user which takes first available square"""

    def tile_to_play(self, game: TicTacToeBoard) -> int:
        return game.free_tiles[0]


def oppenent(player):
    return "o" if player.lower() == "x" else "x"


def test_abstract_player():
    p1 = BasicPlayer("x")
    p2 = BasicPlayer("o")

    assert p1 != p2
    assert p1 == BasicPlayer("x")


@pytest.mark.parametrize(
    "tiles",
    [
        *((i, i + 3, i + 6) for i in range(3)),
        *((i, i + 1, i + 2) for i in range(0, 9, 3)),
        (0, 4, 8),
        (6, 4, 2),
    ],
)
def test_game_loop_winner(tiles: tuple[int]):
    game = TicTacToeBoard()
    player = BasicPlayer("x", *tiles)

    game.game_loop(player)
    assert game.is_finished
    assert game.winner == player


def test_draw():
    game = TicTacToeBoard(["x"] * 9)
    game.game_loop(Dummy("o"), Dummy("x"))
    assert game.is_finished
    assert game.winner is None
