"""Game definition for running TicTacToe with AI using MinMax algorithm"""
import itertools


infinity = 1000000


class Board:
    """Board used to play TicTacToe"""

    def __init__(self):
        self.tile = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
        self.turn_count = 1

    def show_tiles(self):
        """Displays board"""
        for i in range(0, 3):
            offset = i * 3
            # print(offset)
            print(
                str(self.tile[offset])
                + " "
                + str(self.tile[offset + 1])
                + " "
                + str(self.tile[offset + 2])
            )

    def user_turn(self):
        return self.turn_count % 2 != 0

    def turn(self, square: int):
        piece = "x" if self.user_turn() else "o"
        self.tile[square] = piece
        self.turn_count += 1

    def undo_turn(self, square):
        if self.tile[square] == "-":
            print(
                "ERROR UndoTurn: no turn existed in square " + str(square) + " to undo"
            )
            return

        self.tile[square] = "-"
        self.turn_count -= 1

    def squares_free(self):
        free = []
        for x in range(0, 9):
            if self.tile[x] == "-":
                free.append(x)
        return free

    # checks if a given player won
    def has_won(self, player) -> bool:
        """Check if tiles match for a player win condition"""
        horizontals = ((i, i + 2, i + 3) for i in range(0, 3))
        verticals = ((i, i + 3, i + 6) for i in range(0, 3))
        diagonals = ((0, 4, 8), (2, 4, 6))

        for row in itertools.chain(horizontals, verticals, diagonals):
            if all(player == self.tile[i] for i in row):
                return True
        return False


class AI:
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

    def take_turn(self, board: Board) -> int:
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

    def _my_move(self, board: Board, board_index: int):
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

    def _enemy_move(self, board: Board, board_index: int):
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

    def _my_move_rec(self, board: Board, board_index: int):
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


def game_loop():
    # show initial game board
    board = Board()
    cpu1 = AI("o")

    # game initation
    print("***START GAME***")
    board.show_tiles()

    # game main loop
    for _ in range(0, 9):
        if not board.user_turn():
            x = int(input("Enter move: "))
            board.turn(x)
        else:
            cpu_turn = cpu1.take_turn(board)
            board.turn(cpu_turn)

        board.show_tiles()

        for player in ("x", "o"):
            if board.has_won(player):
                print(f"##### {player.upper()!r} wins the game#####")
                break
        else:
            continue
        break

    input("Game Over: Press Enter")
