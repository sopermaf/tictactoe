import logging
import random

import click

from tictactoe.game import AbstractPlayer, TicTacToeBoard

log = logging.getLogger(__name__)


class MaxMinAI(AbstractPlayer):
    def tile_to_play(self, board: TicTacToeBoard) -> int:
        """Return board tile to take turn"""
        click.echo("My Turn!")
        tile_scores = sorted(
            (
                (self._rate_move(board, tile, level=1, is_my_turn=True), tile)
                for tile in board.free_tiles
            ),
            reverse=True,
        )
        top_scores = [t for score, t in tile_scores if score == tile_scores[0][0]]
        log.debug("Scores for Tiles: %s %s", tile_scores, top_scores)

        return random.choice(top_scores)  # noqa: S311

    def _rate_move(
        self,
        board: TicTacToeBoard,
        tile: int,
        level: int,
        *,
        is_my_turn: bool,
    ) -> float:
        """
        Uses max-min algorithm to calculate scores for each of the possible moves.

        Max scores chosen when `is_my_turn` otherwise min scores chosen to simulate
        which move the opponent would choose on their turn.

        The scores are weighted by how far into the future they are, with nearer moves
        receiving higher scores
        """
        copy_board = TicTacToeBoard(board.tiles)
        copy_board.apply_turn(self.token, tile)

        if not copy_board.is_finished:
            move_selector_func = max if is_my_turn else min

            tile_scores = [
                (
                    self._rate_move(
                        board=copy_board,
                        tile=tile,
                        level=level + 1,
                        is_my_turn=not is_my_turn,
                    ),
                    tile,
                )
                for tile in copy_board.free_tiles
            ]

            return move_selector_func(tile_scores)[0]

        # rate the finishing turn scores
        if copy_board.winner is None:
            return 0 / level
        if copy_board.winner == self.token:
            return 1 / level
        return -1 / level
