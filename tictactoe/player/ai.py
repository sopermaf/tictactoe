import logging
import random

import click

from tictactoe.game import AbstractPlayer, TicTacToeBoard

log = logging.getLogger(__name__)


class MaxMinAI(AbstractPlayer):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._enemy = "x" if self.token == "o" else "x"  # noqa: S105

    def tile_to_play(self, board: TicTacToeBoard) -> int:
        """Return board tile to take turn"""
        click.echo("My Turn!")
        tile_scores = sorted(
            ((self._rate_my_move(board, tile, 1), tile) for tile in board.free_tiles),
            reverse=True,
        )
        top_scores = [t for score, t in tile_scores if score == tile_scores[0][0]]
        log.debug("Scores for Tiles: %s %s", tile_scores, top_scores)

        return random.choice(top_scores)  # noqa: S311

    def _rate_my_move(self, board: TicTacToeBoard, tile: int, level: int) -> float:
        """Give me a score if I took this move on the given board"""
        copy_board = TicTacToeBoard(board.tiles)
        copy_board.apply_turn(self.token, tile)

        # rate the move based on their best move
        if not copy_board.is_finished:
            tile_scores = [
                (self._rate_their_move(copy_board, tile, level + 1), tile)
                for tile in copy_board.free_tiles
            ]
            return max(tile_scores)[0]

        # rate the finishing turn scores
        if copy_board.winner is None:
            return 0 / level
        if copy_board.winner == self.token:
            return 1 / level
        return -1 / level

    def _rate_their_move(self, board: TicTacToeBoard, tile: int, level: int) -> float:
        """Give me a score if I took this move on the given board"""
        # simulate the move
        copy_board = TicTacToeBoard(board.tiles)
        copy_board.apply_turn(self._enemy, tile)

        # rate the move based on their best move
        if not copy_board.is_finished:
            tile_scores = [
                (self._rate_my_move(copy_board, tile, level + 1), tile)
                for tile in copy_board.free_tiles
            ]
            return min(tile_scores)[0]

        # rate the finishing turn scores
        if copy_board.winner is None:
            return 0 / level
        if copy_board.winner == self._enemy:
            return -1 / level
        return 1 / level
