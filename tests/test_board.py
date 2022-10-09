"""Test cases for the __main__ module."""
import pytest

from TicTacToe.game import Board


def oppenent(player):
    return "o" if player.lower() == "x" else "x"


@pytest.mark.parametrize(
    "row",
    [
        *((i, i + 1, i + 2) for i in range(0, 3, 3)),
        *((i, i + 3, i + 6) for i in range(0, 3, 3)),
        (0, 4, 8),
        (6, 4, 2),
    ],
)
def test_has_won(row):
    board = Board()
    for player in ("x", "o"):
        for i in row:
            board.tile[i] = player
        assert board.has_won(player)
        assert not board.has_won(oppenent(player))
