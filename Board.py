class Board:
	def __init__(self, fn):
		default = [1,2,3,4,5,6,7,8,9];
		self.board = [[default[:] for j in range(9)] for i in range (9)];

		self.readFile(fn);



	def readFile(self, fn):
		f = open(fn, 'r');

		r = 0;
		while r < 9:
			line = f.readline().strip().split();
			c = 0;
			while c < 9:
				val = int(line[c]);
				if val != 0:
					self.board[r][c] = [val];
					self.constrainRows(r, c, val);
					self.constrainCols(r, c, val);
					self.constrainBox(r, c, val);
					if not (((r % 4) == 0) or ((c % 4) == 0)):
						self.constrainHyper(r, c, val);

					#if any cell has an empty domain, FAIL
				c += 1;
			r += 1;

		f.close();
		return


	def constrainRows(self, r, c, val):
		for i in range(9):
			# domain = self.board[r][i];
			if (val in self.board[r][i]) and (i != c):
				self.board[r][i].remove(val);
			#print(domain);


	def constrainCols(self, r, c, val):
		for i in range(9):
			if val in self.board[i][c] and (i!= r):
				self.board[i][c].remove(val);


	def constrainBox(self, r, c, val):
		cQ = c // 3;
		rQ = r // 3;
		i = 0;
		while i < 3:
			j = 0;
			while j < 3:
				queryR = (3 * rQ) + i;
				queryC = (3 * cQ) + j;
				if val in self.board[queryR][queryC] and not((queryR == r) and (queryC == c)):
					#print((queryR, queryC))
					self.board[queryR][queryC].remove(val);
				j += 1;
			i += 1;


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
				if val in self.board[i][j] and not ((r == i) and (c == j)):
					self.board[i][j].remove(val)
				j += 1
			i += 1


	def get(self, row, col):
		return self.board[row][col]


	def __str__(self):
		out = ''
		for row in self.board:
			for col in row:
				out += str(col) + ' ';
			out += '\n\n';
		return out;

#MRV
#go thorugh everyhting and find the minimum
#keep locations of the minimum in maybe a list?
#Needs a priotiry queue ordered by size of domain
#The queue should return a list of variables with the smallest domains


#DEGREE
#go through the list of locations and check direct neighbors to find best one?
#keep the min of that in a list as well??? 
#if there are multiple with the same degree, then we just choose the first one bc arbitrary\
#This should take the list given by MRV and choose the variable with the least unassigned neighbors
#Neighbors can be found in constant time by using the same loops in the constrain functions
#	(Always checks 9 variables per row, col, box, and maybe hyper)
#Whatever variables it doesn't choose should be put back in the MRV heap

#backtracking (recursive)
#constantly have to run the contraints, if it ever happens so that a box is empty, we return [] or seomthing
#and go back and replace the thing with the next number in the domain
#i guess



def selectUnassigned(board, assignment):
	restrained = mrv(board, assignment);
	out = degree(restrained, assignment);
	return out;


def mrv(board, assignment):
	out = [];
	minSize, minR, minC = 10, 10, 10;
	r = 0
	while r < 9:
		c = 0
		while c < 9:
			if assignment[r][c] == 0:
				if len(board.get(r, c)) == minSize:
					out.append((r, c));

				if len(board.get(r, c)) < minSize:
					out = [(r, c)];
					minSize = len(board.get(r, c));

			c += 1
		r += 1
	return out


def degree(restrained, assignment):
	maxN = 0; #Number of unassigned neighmors
	maxR, maxC = 0, 0; #Location of variable with most unassigned neighbors
	for var in restrained: #var = (r, c)
		varR, varC = var[0], var[1]
		if checkNeighbors(varR, varC, assignment) > maxN:
			maxR, maxC = varR, varC
	return (maxR, maxC)


# def isConsistent(val, r, c, assignment):
# 	if val in r, c, box, hyper:
# 		return false

def addAssignment():
	pass


def removeAssignment():
	pass


def complete():
	pass


def checkRow(row, assigment):
	checked = set();
	i = 0;
	while i < 9:
		if assignment[row][i] == 0:
			checked.add((row, i));
		i += 1;
	return checked;


def checkCol(col, assigment):
	checked = set();
	i = 0;
	while i < 9:
		if assignment[i][col] == 0:
			checked.add((i, col));
		i += 1;
	return checked;


def checkBox(row, col, assignment):
	checked = set();
	tempR = row // 3;
	tempC = col // 3;

	tempR = tempR * 3;
	tempC = tempC * 3;

	i = tempR;
	while i < tempR + 3:
		j = tempC;
		while j < tempC + 3:
			if assignment[i][j] == 0:
				checked.add((i, j));
			j += 1;
		i += 1;
	return checked;


def checkHyper(row, col, assignment):
	checked = set();
	tempR = row // 4 # if this is 0, then it's the first one , if its 1 then its the second half 
	tempC = col // 4 # 4 * tempR + 1  < 4 * tempR + 4
	# less than three!
	tempR = tempR * 4 + 1
	tempC = tempC * 4 + 1

	i = tempR
	while i < tempR + 3:
		j = tempC
		while j < tempC + 3:
			if assignment[i][j] == 0:
				checked.add((i, j));
			j += 1
		i += 1
	return checked;


def checkNeighbors(row, col, assignment):
	count = set();
	count = count.union(checkRow(row, assignment));
	count = count.union(checkCol(col, assignment));
	count = count.union(checkBox(row, col, assignment));
	if not (((row % 4) == 0) or ((col % 4) == 0)):
		count = count.union(checkHyper(row, col, assignment));
	print('%d %d %d' % (row, col, len(count)-1))
	return len(count) - 1;


def backtrack(board, assignment):
	if complete(assignment):
		return ('Hooray', assignment);
	var = selectUnassigned(board, assignment); #var = (r, c) for best variable



board = Board('test.txt');
print(board);
assignment = [([0] * 9) for i in range(9)];

print(selectUnassigned(board, assignment))