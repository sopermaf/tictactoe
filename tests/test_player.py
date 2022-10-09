from TicTacToe.game import AbstractPlayer, Game
from TicTacToe.player import AI


class Dummy(AbstractPlayer):
    def decide_turn(self, game: Game) -> int:
        return game.squares_free()[0]


def test_full_game():
    game = Game()
    # TODO: the self AI is backwards
    game.run_game(AI("o"), Dummy())
    assert game.has_won("x")
