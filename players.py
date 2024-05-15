import random
import time
import pygame
import numpy as np
import math
from connect4 import connect4
from copy import deepcopy
#Ethan Park
class connect4Player(object):
	def __init__(self, position, seed=0, CVDMode=False):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)
		if CVDMode:
			global P1COLOR
			global P2COLOR
			P1COLOR = (227, 60, 239)
			P2COLOR = (0, 255, 0)

	def play(self, env: connect4, move: list) -> None:
		move = [-1]

class human(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					#sys.exit()
					print("hi")

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):
	
	def horizontalCheck(self, board, piece):
		score = 0
		if piece == 1:
			opp_piece = 2
		else:
			opp_piece = 1
		for i in range(ROW_COUNT):
			for j in range(COLUMN_COUNT - 3):
				pcount = 0
				oppcount = 0
				zcount = 0
				for k in range(4):
					if board[i][j+k] == piece:
						pcount += 1
					elif board[i][j+k] == opp_piece:
						oppcount += 1
					elif board[i][j+k] == 0:
						zcount += 1
				if pcount == 4:
					score+= 1000
				elif pcount == 3 and zcount == 1:
					score += 10
				elif pcount == 2 and zcount == 2:
					score += 2
				if oppcount == 4:
					score -= 1000
				elif oppcount == 3 and zcount == 1:
					score -= 10
				elif oppcount == 2 and zcount == 2:
					score -= 2

		return score
	
	def verticalCheck(self, board, piece):
		score = 0
		if piece == 1:
			opp_piece = 2
		else:
			opp_piece = 1
		for i in range(ROW_COUNT - 3, ROW_COUNT):
			for j in range(COLUMN_COUNT):
				pcount = 0
				oppcount = 0
				zcount = 0
				for k in range(4):
					if board[i-k][j] == piece:
						pcount += 1
					elif board[i-k][j] == opp_piece:
						oppcount += 1
					elif board[i-k][j] == 0:
						zcount += 1
				if pcount == 4:
					score+= 1000
				elif pcount == 3 and zcount == 1:
					score += 10
				elif pcount == 2 and zcount == 2:
					score += 2
				if oppcount == 4:
					score -= 1000
				elif oppcount == 3 and zcount == 1:
					score -= 10
				elif oppcount == 2 and zcount == 2:
					score -= 2
		return score

	def RDiagCheck(self, board, piece):
		score = 0
		if piece == 1:
			opp_piece = 2
		else:
			opp_piece = 1

		for i in range(ROW_COUNT - 3):
			for j in range(COLUMN_COUNT - 3):
				pcount = 0
				oppcount = 0
				zcount = 0
				for k in range(4):
					if board[i+k][j+k] == piece:
						pcount += 1
					elif board[i+k][j+k] == opp_piece:
						oppcount += 1
					elif board[i+k][j+k] == 0:
						zcount += 1
				if pcount == 4:
					score+= 1000
				elif pcount == 3 and zcount == 1:
					score += 10
				elif pcount == 2 and zcount == 2:
					score += 2
				if oppcount == 4:
					score -= 1000
				elif oppcount == 3 and zcount == 1:
					score -= 10
				elif oppcount == 2 and zcount == 2:
					score -= 2
		return score

	def LDiagCheck(self, board, piece):
		score = 0
		if piece == 1:
			opp_piece = 2
		else:
			opp_piece = 1
		for i in range(ROW_COUNT - 3, ROW_COUNT):
			for j in range(COLUMN_COUNT - 3):
				pcount = 0
				oppcount = 0
				zcount = 0
				for k in range(4):
					if board[i-k][j+k] == piece:
						pcount += 1
					elif board[i-k][j+k] == opp_piece:
						oppcount += 1
					elif board[i-k][j+k] == 0:
						zcount += 1
				if pcount == 4:
					score+= 1000
				elif pcount == 3 and zcount == 1:
					score += 10
				elif pcount == 2 and zcount == 2:
					score += 2
				if oppcount == 4:
					score -= 1000
				elif oppcount == 3 and zcount == 1:
					score -= 10
				elif oppcount == 2 and zcount == 2:
					score -= 2
		return score
	#evaluates current stae of the board
	def evaluationFunction(self, board, piece):
		score = 0
		score+=self.horizontalCheck(board,piece)
		score+=self.verticalCheck(board,piece)
		score+=self.RDiagCheck(board,piece)
		score+=self.LDiagCheck(board,piece)
		return score
	#simulate a move
	def simulateMove(self, env: connect4, move: int, player: int):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)
	#Max function
	def Max(self, env: connect4, depth, checker):
		if depth == 0: #reach depth
			return None, self.evaluationFunction(env.board, checker)
		possible = env.topPosition >= 0
		indices = []
		for i,p in enumerate(possible):
			if p:
				indices.append(i)
		move = random.choice(indices)
		value = -np.inf
		for column in indices:
			envCopy = deepcopy(env)
			self.simulateMove(envCopy, column, envCopy.turnPlayer.position)
			envCopy.turnPlayer = envCopy.turnPlayer.opponent
			_, score = self.Min(envCopy, depth - 1, checker)
			if score > value: #update if better score is found
				value = score
				move = column
		return move, value
	#Min function
	def Min(self, env: connect4, depth, checker):
		if depth == 0: #reach depth
			return None, self.evaluationFunction(env.board, checker)
		possible = env.topPosition >= 0
		indices = []
		for i,p in enumerate(possible):
			if p:
				indices.append(i)
		move = random.choice(indices)
		value = np.inf
		for column in indices:
			envCopy = deepcopy(env)
			self.simulateMove(envCopy, column, envCopy.turnPlayer.position)
			envCopy.turnPlayer = envCopy.turnPlayer.opponent
			move, score = self.Max(envCopy, depth - 1, checker)
			if score < value: #update if better score is found
				value = score
		return move, value
	
	#start
	def play(self, env: connect4, move: list) -> None:
		depth = 2
		checker = self.position
		column, value = self.Max(env, depth, checker)
		move[:] = [column]
		pass


class alphaBetaAI(connect4Player):
	def simulateMove(self, env: connect4, move: int, player: int):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)

	def horizontalCheck(self, board, piece):
		score = 0
		if piece == 1:
			opp_piece = 2
		else:
			opp_piece = 1
		for i in range(ROW_COUNT):
			for j in range(COLUMN_COUNT - 3):
				pcount = 0
				oppcount = 0
				zcount = 0
				for k in range(4):
					if board[i][j+k] == piece:
						pcount += 1
					elif board[i][j+k] == opp_piece:
						oppcount += 1
					elif board[i][j+k] == 0:
						zcount += 1
				if pcount == 4:
					score+= 1000
				elif pcount == 3 and zcount == 1:
					score += 10
				elif pcount == 2 and zcount == 2:
					score += 2
				if oppcount == 4:
					score -= 1000
				elif oppcount == 3 and zcount == 1:
					score -= 10
				elif oppcount == 2 and zcount == 2:
					score -= 2

		return score
	
	def verticalCheck(self, board, piece):
		score = 0
		if piece == 1:
			opp_piece = 2
		else:
			opp_piece = 1
		for i in range(ROW_COUNT - 3, ROW_COUNT):
			for j in range(COLUMN_COUNT):
				pcount = 0
				oppcount = 0
				zcount = 0
				for k in range(4):
					if board[i-k][j] == piece:
						pcount += 1
					elif board[i-k][j] == opp_piece:
						oppcount += 1
					elif board[i-k][j] == 0:
						zcount += 1
				if pcount == 4:
					score+= 1000
				elif pcount == 3 and zcount == 1:
					score += 10
				elif pcount == 2 and zcount == 2:
					score += 2
				if oppcount == 4:
					score -= 1000
				elif oppcount == 3 and zcount == 1:
					score -= 10
				elif oppcount == 2 and zcount == 2:
					score -= 2
		return score

	def RDiagCheck(self, board, piece):
		score = 0
		if piece == 1:
			opp_piece = 2
		else:
			opp_piece = 1
		for i in range(ROW_COUNT - 3):
			for j in range(COLUMN_COUNT - 3):
				pcount = 0
				oppcount = 0
				zcount = 0
				for k in range(4):
					if board[i+k][j+k] == piece:
						pcount += 1
					elif board[i+k][j+k] == opp_piece:
						oppcount += 1
					elif board[i+k][j+k] == 0:
						zcount += 1
				if pcount == 4:
					score+= 1000
				elif pcount == 3 and zcount == 1:
					score += 10
				elif pcount == 2 and zcount == 2:
					score += 2
				if oppcount == 4:
					score -= 1000
				elif oppcount == 3 and zcount == 1:
					score -= 10
				elif oppcount == 2 and zcount == 2:
					score -= 2
		return score

	def LDiagCheck(self, board, piece):
		score = 0
		if piece == 1:
			opp_piece = 2
		else:
			opp_piece = 1
		for i in range(3, ROW_COUNT):
			for j in range(COLUMN_COUNT - 3):
				pcount = 0
				oppcount = 0
				zcount = 0
				for k in range(4):
					if board[i-k][j+k] == piece:
						pcount += 1
					elif board[i-k][j+k] == opp_piece:
						oppcount += 1
					elif board[i-k][j+k] == 0:
						zcount += 1
				if pcount == 4:
					score+= 1000
				elif pcount == 3 and zcount == 1:
					score += 10
				elif pcount == 2 and zcount == 2:
					score += 2
				if oppcount == 4:
					score -= 1000
				elif oppcount == 3 and zcount == 1:
					score -= 10
				elif oppcount == 2 and zcount == 2:
					score -= 2
		return score

	def evaluationFunction(self, board, piece):
		score = 0
		score+=self.horizontalCheck(board,piece)
		score+=self.verticalCheck(board,piece)
		score+=self.RDiagCheck(board,piece)
		score+=self.LDiagCheck(board,piece)
		return score

	#Generate list of successor moves, favoring center column
	def succ_func(self, indices):
		succ = []
		center_column = COLUMN_COUNT // 2
		if center_column in indices:
			succ.append(center_column)
		for col in indices:
			if col != center_column:
				succ.append(col)

		return succ
	#Max function
	def Max(self, env: connect4, depth, checker, alpha, beta):
		if depth == 0: #reach depth
			return 0, self.evaluationFunction(env.board, checker)
		
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p:
				indices.append(i)

		indices = self.succ_func(indices)
		
		move = random.choice(indices)
		value = -np.inf
		for column in indices:
			envCopy = deepcopy(env)
			self.simulateMove(envCopy, column, envCopy.turnPlayer.position)
			envCopy.turnPlayer = envCopy.turnPlayer.opponent
			_, score = self.Min(envCopy, depth - 1, checker, alpha, beta)
			if score > value:
				value = score
				move = column
			if beta <= value: #Pruning
				return move, value
			if value > alpha: #update alpha
				alpha = value

		return move, value
	
		
	def Min(self, env: connect4, depth, checker, alpha, beta):
		if depth == 0: #reach depth
			return 0, self.evaluationFunction(env.board, checker)
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p:
				indices.append(i)

		indices = self.succ_func(indices)

		value = np.inf
		for column in indices:
			envCopy = deepcopy(env)
			self.simulateMove(envCopy, column, envCopy.turnPlayer.position)
			envCopy.turnPlayer = envCopy.turnPlayer.opponent
			move, score = self.Max(envCopy, depth - 1, checker, alpha, beta)
			if score < value:
				value = score
			if alpha >= value: #Pruning
				return move, value
			if value < beta: #update beta
				beta = value
		return move, value
		
	def play(self, env: connect4, move: list) -> None:
		depth = 2
		checker = self.position
		column, _ = self.Max(env, depth, checker, -np.inf, np.inf)
		move[:] = [column]


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
P1COLOR = (255,0,0)
P2COLOR = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
