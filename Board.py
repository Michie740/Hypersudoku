class Board:
	# initilizing board with domains
	def __init__(self, fn):
		default = [1,2,3,4,5,6,7,8,9]
		self.board = [[default[:] for j in range(9)] for i in range (9)]

		self.readFile(fn)


	# reading file and restricing domains based on the initial file
	def readFile(self, fn):
		f = open(fn, 'r')
		r = 0
		while r < 9:
			line = f.readline().strip().split()
			c = 0
			while c < 9:
				val = int(line[c])
				if val != 0:
					self.board[r][c] = [val]
					self.constrainRows(r, c, val)
					self.constrainCols(r, c, val)
					self.constrainBox(r, c, val)
					if not (((r % 4) == 0) or ((c % 4) == 0)):
						self.constrainHyper(r, c, val)
				c += 1
			r += 1
		f.close()
		return


		# constrain domain based on rows
	def constrainRows(self, r, c, val):
		for i in range(9):
			if (val in self.board[r][i]) and (i != c):
				self.board[r][i].remove(val)

		# constrain domain based on columns
	def constrainCols(self, r, c, val):
		for i in range(9):
			if val in self.board[i][c] and (i!= r):
				self.board[i][c].remove(val)


		# constrain domain based on boxes
	def constrainBox(self, r, c, val):
		cQ = c // 3
		rQ = r // 3
		i = 0
		while i < 3:
			j = 0
			while j < 3:
				queryR = (3 * rQ) + i
				queryC = (3 * cQ) + j
				# if val is in box remove from domain
				if val in self.board[queryR][queryC] and not((queryR == r) and (queryC == c)):
					self.board[queryR][queryC].remove(val)
				j += 1
			i += 1


		# contrain domain based on hyperboxes
	def constrainHyper(self, r, c, val):
		#4 and 8!
		#r can be 1 2 3 | 5 6 7
		#c can be 1 2 3 | 5 6 7
		
		#r and c of the value we are trying to replace
		tempR = r // 4 # if this is 0, then it's the first one , if its 1 then its the second half 
		tempC = c // 4 # 4 * tempR + 1  < 4 * tempR + 4
		# less than three!
		tempR = tempR * 4 + 1
		tempC = tempC * 4 + 1

		i = tempR
		while i < tempR + 3:
			j = tempC
			while j < tempC + 3:
				# if the number is in the hyperbox remove from domain
				if val in self.board[i][j] and not ((r == i) and (c == j)):
					self.board[i][j].remove(val)
				j += 1
			i += 1


	# getting 
	def get(self, row, col):
		return self.board[row][col]


	# print board
	def __str__(self):
		out = ''
		for row in self.board:
			for col in row:
				out += str(col) + ' '
			out += '\n\n'
		return out