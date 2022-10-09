
infinity = 1000000

class Board:
	def __init__(self):
		self.tile = ['-','-','-','-','-','-','-','-','-']
		self.turn_count = 1
		
	def show_tiles(self):
		for i in range(0,3):
			offset = i * 3
			# print(offset)
			print(str(self.tile[offset]) + " " + str(self.tile[offset+1]) + " " + str(self.tile[offset+2]))
	
	def user_turn(self):
		if self.turn_count%2==0:
			return False
		return True
	
	def turn(self, square):
		piece = 'x'
		if self.user_turn() == True:
			piece = 'o'
		self.tile[square] = piece
		self.turn_count += 1
	
	def undoTurn(self, square):
		if self.tile[square] == '-':
			print("ERROR UndoTurn: no turn existed in square " + str(square) + " to undo")
			return
			
		self.tile[square] = '-'
		self.turn_count -= 1
				
	def squares_free(self):
		free = []
		for x in range(0,9):
			if self.tile[x] == '-':
				free.append(x)
		return free
	
	#checks if a given player won
	def checkWin(self, type):
		#horizontal
		for x in range(0,3):
			offset = x * 3
			if type == self.tile[offset] and type == self.tile[offset+1] and type == self.tile[offset+2]:
				return True
		#vertical
		for x in range(0,3):
			if type == self.tile[x] and type == self.tile[x+3] and type == self.tile[x+6]:
				return True
		#diagonal
		if type == self.tile[0] and type == self.tile[4] and type == self.tile[8]:
				return True
		if type == self.tile[2] and type == self.tile[4] and type == self.tile[6]:
				return True

stack = []
				
class AI:
	def __init__(self, type):
		self.type = type
		self.level = 0
		self.nextMoveFlag = -1	#-1 if no next move win
		self.nextMoveWin = False #so as winning moves aren't overwritten with moves that only prevent opponent wins
		
		if type == 'o':
			self.enemy = 'x'
		else:
			self.enemy = 'o'
	
	#just returns first available move
	def takeTurn(self, board):
		bestMove = self.decideMove(board)
		print("AI chooses move " + str(bestMove))
		return bestMove
		
	def decideMove(self, board):
		possMoves = board.squares_free()
		possMovesScore = []
		
		#rate each Move
		for move in possMoves:
			board.turn(move)
			moveScore = self.myMove(board, move)
			board.undoTurn(move)
			possMovesScore.append(moveScore)
			
		#find best move
		bestMoveIndex = 0
		print("Move ratings: " + str(possMovesScore))
		#print("Rate available moves")
		for i in range(0, len(possMovesScore)):
			if possMovesScore[bestMoveIndex] < possMovesScore[i]:
				bestMoveIndex = i
		#take the max move
		
		#check for next move wins/losses
		if self.nextMoveFlag != -1:
			print("Next Move Flag for board position: " + str(self.nextMoveFlag))
			bestMoveIndex = possMoves.index(self.nextMoveFlag)	#change the index
			self.nextMoveFlag = -1
			self.nextMoveWin = False
		
		return possMoves[bestMoveIndex]	#squareNumber of bestMove
	
	def myMove(self, board, boardIndex):
		self.level += 1
		moveScore = -100
		if board.checkWin(self.type):
			if self.level == 1:
				self.nextMoveFlag = boardIndex
				self.nextMoveWin = True
			moveScore = 1
		elif board.checkWin(self.enemy):
			moveScore = -1
		elif len(board.squares_free()) < 1:
			moveScore = 0	#draw
		else:
			possMoves = board.squares_free()
			moveScores = []	#array of possibilities
			#get all possible scores
			for move in possMoves:
				board.turn(move)
				moveScores.append(self.enemyMove(board, move))
				board.undoTurn(move)	#reset board
			
			#get Max possible
			print("Possible Scores: " + str(moveScores))
			for score in moveScores:
				if moveScore < score:
					moveScore = score
			print("Chosen Max Score: " + str(moveScore))
		
		self.level -= 1
		return moveScore
	
	def enemyMove(self, board, boardIndex):
		self.level += 1
		moveScore = 100
		if board.checkWin(self.type):
			moveScore = -1
		elif board.checkWin(self.enemy):
			if self.level == 2 and not self.nextMoveWin: #nextMoveWin for enemy
				self.nextMoveFlag = boardIndex
			moveScore = 1
		elif len(board.squares_free()) < 1:
			moveScore = 0	#draw
		else:
			possMoves = board.squares_free()
			moveScores = []	#array of possibilities
			#get all possible scores
			for move in possMoves:
				board.turn(move)
				moveScores.append(self.enemyMove(board, move))
				board.undoTurn(move)	#reset board
			
			#get min possible
			#print("Possible Scores: " + str(moveScores))
			for score in moveScores:
				if moveScore > score:
					moveScore = score
			#print("Chosen Min Score: " + str(moveScore))
			
		self.level -= 1
		return moveScore
	
	def myMoveRec(self, board, boardIndex):
		self.level += 1
		moveScore = 0
		if board.checkWin(self.type):
			if self.level == 1: #nextMoveWin for enemy
				self.nextMoveFlag = boardIndex
				self.nextMoveWin = True
			moveScore = 1/self.level
		elif board.checkWin(self.enemy):
			if self.level == 2 and not self.nextMoveWin: #nextMoveWin for enemy
				self.nextMoveFlag = boardIndex
			moveScore = -1
		elif len(board.squares_free()) < 1:	#already know a win didn't occur
			moveScore = 0	#draw
		else:
			possMoves = board.squares_free()
			for move in possMoves:
				board.turn(move)
				moveScore += self.myMoveRec(board, move)
				board.undoTurn(move)	#reset board	
		self.level -= 1
		return moveScore
	
	def showDetails(self):
		print("AI is " + self.type)


def game_loop():
	#show initial game board
	board = Board()
	cpu1 = AI('o')

	#game initation
	cpu1.showDetails()
	print("***START GAME***")
	board.show_tiles()

	#game main loop
	for game_turn in range(0,9):
		#check turn
		if not board.user_turn():
			#make user move
			x = int(input("Enter move: "))
			board.turn(x)
		else:
			#computer move
			cpuTurn = cpu1.takeTurn(board)
			#x = int(input("Enter move: "))
			board.turn(cpuTurn)
		
		board.show_tiles()
		
		#check win
		if board.checkWin('x'):
			print('##### X wins the game#####')
			break
		elif board.checkWin('o'):
			print('##### O wins the game#####')
			break

	input("Game Over: Press Enter")
