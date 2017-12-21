
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
			#make move
			board.turn(move)
			#score move
			moveScore = self.decideMoveRecursive(board)
			#undo move
			board.undoTurn(move)
			#add score to list
			possMovesScore.append(moveScore)
		#maxMove
		bestMoveIndex = 0
		print("Move ratings: " + str(possMovesScore))
		#print("Rate available moves")
		for i in range(0, len(possMovesScore)):
			if possMovesScore[bestMoveIndex] < possMovesScore[i]:
				bestMoveIndex = i
		#take the max move
		return possMoves[bestMoveIndex]	#squareNumber of bestMove
		
	def decideMoveRecursive(self, board):
		moveScore = 0
		#print("Recursion level START:" + str(self.level))
		if board.checkWin(self.type):
		#	print("self simulation win")
			moveScore = 1
		elif board.checkWin(self.enemy):
		#	print("self simulation loss")
			moveScore = -1
		elif len(board.squares_free()) < 1:	#already know a win didn't occur
		#	print("self simulation draw")
			moveScore = 0	#draw
		else:
			possMoves = board.squares_free()
			
			for move in possMoves:
		#		print("*before move " + str(move) + "*")
				board.turn(move)
		#		board.show_tiles()
				stack.append(move)
		#		print(stack)
				self.level += 1
				moveScore += self.decideMoveRecursive(board)
				self.level -= 1
		#		print("*after move " + str(move) + " - score: " + str(moveScore) + "*")
				stack.pop()
				board.undoTurn(move)	#reset board
				#board.show_tiles()
				
		#result of function
		#print("Recursion level END:" + str(self.level))
		return moveScore
	
	def showDetails(self):
		print("AI is " + self.type)



#show initial game board
board = Board()
cpu1 = AI('x')

#game initation
cpu1.showDetails()
print("***START GAME***")
board.show_tiles()

#game main loop
for game_turn in range(0,9):
	#check turn
	if board.user_turn():
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
		print('X wins the game')
		break
	elif board.checkWin('o'):
		print('O wins the game')
		break

print("Program finished 305")
input("Press Enter")
