"""Test cases for the __main__ module."""

import pytest

from tictactoe.game import AbstractPlayer, Game


class User(AbstractPlayer):
    def __init__(self, *moves) -> None:
        self.moves = iter(moves)
        super().__init__()

    def decide_turn(self, game) -> int:
        return next(self.moves)


def oppenent(player):
    return "o" if player.lower() == "x" else "x"


@pytest.mark.parametrize(
    "row",
    [
        *[(i, i + 1, i + 2) for i in range(0, 9, 3)],
        *((i, i + 3, i + 6) for i in range(3)),
        (0, 4, 8),
        (6, 4, 2),
    ],
)
def test_has_won(row):
    for player in ("x", "o"):
        game = Game()
        for i in row:
            game.tile[i] = player
        assert game.has_won(player)
        assert not game.has_won(oppenent(player))


@pytest.mark.parametrize(
    ("occupied", "exp"),
    [
        (range(9), []),
        ([], range(9)),
        ([0, 1], range(2, 9)),
        ([7, 8], range(7)),
    ],
)
def test_squares_free(occupied, exp):
    game = Game()
    for square in occupied:
        game.turn(square)

    assert sorted(game.squares_free()) == list(exp)


@pytest.mark.parametrize(
    ("player_1", "player_2", "winner"),
    [
        (User(0, 1, 2), User(3, 5), "x"),
        (User(0, 2, 7), User(3, 5, 4), "o"),
    ],
)
def test_full_game(player_1, player_2, winner):
    game = Game()
    game.run_game(player_1, player_2)
    assert game.has_won(winner)
