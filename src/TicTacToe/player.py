from TicTacToe.game import AbstractPlayer, Game


class TerminalUser(AbstractPlayer):
    def decide_turn(self, _) -> int:
        return int(input("Enter turn (0-8): "))


class AI(AbstractPlayer):
    """Computer TicTacToe Player"""

    def __init__(self, type):
        self.type = type
        self.level = 0
        self.next_move_flag = -1  # -1 if no next move win
        # so as winning moves aren't overwritten with moves
        # that only prevent opponent wins
        self.next_move_win = False

        if type == "o":
            self.enemy = "x"
        else:
            self.enemy = "o"

    def decide_turn(self, board: Game) -> int:
        """Return board tile to take turn"""
        poss_moves = board.squares_free()
        poss_moves_score = []

        # rate each Move
        print("Thinking ...")
        for move in poss_moves:
            board.turn(move)
            move_score = self._my_move(board, move)
            board.undo_turn(move)
            poss_moves_score.append(move_score)

        # find best move
        best_move_index = 0
        # print("Move ratings: " + str(possMovesScore))
        # print("Rate available moves")
        for i in range(0, len(poss_moves_score)):
            if poss_moves_score[best_move_index] < poss_moves_score[i]:
                best_move_index = i
        # take the max move

        # check for next move wins/losses
        if self.next_move_flag != -1:
            print("Next Move Flag for board position: " + str(self.next_move_flag))
            best_move_index = poss_moves.index(self.next_move_flag)  # change the index
            self.next_move_flag = -1
            self.next_move_win = False

        print("I know!")
        return poss_moves[best_move_index]  # squareNumber of bestMove

    def _my_move(self, board: Game, board_index: int):
        self.level += 1
        move_score = -100
        if board.has_won(self.type):
            if self.level == 1:
                self.next_move_flag = board_index
                self.next_move_win = True
            move_score = 1
        elif board.has_won(self.enemy):
            move_score = -1
        elif len(board.squares_free()) < 1:
            move_score = 0  # draw
        else:
            poss_moves = board.squares_free()
            move_scores = []  # array of possibilities
            # get all possible scores
            for move in poss_moves:
                board.turn(move)
                move_scores.append(self._enemy_move(board, move))
                board.undo_turn(move)  # reset board

            # get Max possible
            # print("Possible Scores: " + str(moveScores))
            for score in move_scores:
                if move_score < score:
                    move_score = score
            # print("Chosen Max Score: " + str(moveScore))

        self.level -= 1
        return move_score

    def _enemy_move(self, board: Game, board_index: int):
        self.level += 1
        move_score = 100
        if board.has_won(self.type):
            move_score = -1
        elif board.has_won(self.enemy):
            if self.level == 2 and not self.next_move_win:  # nextMoveWin for enemy
                self.next_move_flag = board_index
            move_score = 1
        elif len(board.squares_free()) < 1:
            move_score = 0  # draw
        else:
            poss_moves = board.squares_free()
            move_scores = []  # array of possibilities
            # get all possible scores
            for move in poss_moves:
                board.turn(move)
                move_scores.append(self._enemy_move(board, move))
                board.undo_turn(move)  # reset board

            # get min possible
            # print("Possible Scores: " + str(moveScores))
            for score in move_scores:
                if move_score > score:
                    move_score = score
            # print("Chosen Min Score: " + str(moveScore))

        self.level -= 1
        return move_score

    def _my_move_rec(self, board: Game, board_index: int):
        self.level += 1
        move_score = 0
        if board.has_won(self.type):
            if self.level == 1:  # nextMoveWin for enemy
                self.next_move_flag = board_index
                self.next_move_win = True
            move_score = 1 / self.level
        elif board.has_won(self.enemy):
            if self.level == 2 and not self.next_move_win:  # nextMoveWin for enemy
                self.next_move_flag = board_index
            move_score = -1
        elif len(board.squares_free()) < 1:  # already know a win didn't occur
            move_score = 0  # draw
        else:
            poss_moves = board.squares_free()
            for move in poss_moves:
                board.turn(move)
                move_score += self._my_move_rec(board, move)
                board.undo_turn(move)  # reset board
        self.level -= 1
        return move_score
