import pytest

from tictactoe.game import TicTacToeBoard
from tictactoe.player.ai import MaxMinAI


@pytest.mark.parametrize(
    "initial_board",
    [
        [
            "x",
            "o",
            "x",
            "-",
            "x",
            "o",
            "-",
            "-",
            "-",
        ],
        [
            "-",
            "o",
            "x",
            "-",
            "x",
            "-",
            "-",
            "o",
            "-",
        ],
        [
            "-",
            "-",
            "x",
            "o",
            "x",
            "-",
            "-",
            "-",
            "o",
        ],
        [
            "-",
            "o",
            "x",
            "-",
            "o",
            "x",
            "-",
            "-",
            "-",
        ],
    ],
)
def test_choose_next_winning_move(initial_board: list[str]):
    # setup board 1 turn away from a win
    board = TicTacToeBoard(initial_board)
    ai = MaxMinAI("x")

    chosen_tile = ai.tile_to_play(board)
    board.apply_turn(ai.token, chosen_tile)
    assert board.is_finished
    assert board.winner == ai


@pytest.mark.parametrize(
    "initial_board",
    [
        [
            "x",
            "-",
            "-",
            "-",
            "o",
            "-",
            "o",
            "-",
            "x",
        ],
    ],
)
def test_block_opponent_winning_move(initial_board: list[str]):
    # setup board 1 turn away from a win
    board = TicTacToeBoard(initial_board)
    ai = MaxMinAI("x")

    chosen_tile = ai.tile_to_play(board)
    board.apply_turn(ai.token, chosen_tile)
    assert not board.is_finished
    assert board.tiles[2] == ai.token


def test_unbeatable():
    """Two MaxMinAIs should always draw"""
    board = TicTacToeBoard()
    board.game_loop(MaxMinAI("x"), MaxMinAI("o"))
    assert board.is_finished
    assert board.winner is None
