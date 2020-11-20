from Board import Board

# choosing next best variable based on 2 heuristics
def selectUnassigned(board, assignment):
	restrained = mrv(board, assignment);
	out = degree(restrained, assignment);
	return out;


# most restrained variables (choosing a list of the variables with the smallest domains)
def mrv(board, assignment):
	out = [];
	minSize, minR, minC = 10, 10, 10;
	r = 0
	while r < 9:
		c = 0
		while c < 9:
			if assignment[r][c] == 0: #If variable at (r, c) is unassigned
				# if that domain is the smallest domain, then fill our list with it
				if len(board.get(r, c)) == minSize:
					out.append((r, c));
				# if its smaller then the domain of whats in the list, then replace it
				if len(board.get(r, c)) < minSize:
					out = [(r, c)];
					minSize = len(board.get(r, c));

			c += 1
		r += 1
	return out

# most unassigned neighbors
def degree(restrained, assignment):
	maxN = -1; #Number of unassigned neighmors
	maxR, maxC = 0, 0; #Location of variable with most unassigned neighbors
	for var in restrained: #var = (r, c)
		varR, varC = var[0], var[1]
		#finding the one with the most unassigned neightbors (maxN) from list giben by mrv
		if checkNeighbors(varR, varC, assignment) > maxN:
			maxR, maxC = varR, varC
	#returns r c (location of that place)
	return (maxR, maxC);

#counting neighbors (for degree)
def checkNeighbors(row, col, assignment):
	count = set();
	count = count.union(checkRow(row, assignment));
	count = count.union(checkCol(col, assignment));
	count = count.union(checkBox(row, col, assignment));
	if not (((row % 4) == 0) or ((col % 4) == 0)):
		count = count.union(checkHyper(row, col, assignment));
	return len(count) - 1;

# checkNeighbors helper (counts unaddigned neighbors in row)
def checkRow(row, assigment):
	checked = set();
	i = 0;
	while i < 9:
		if assignment[row][i] == 0:
			checked.add((row, i));
		i += 1;
	return checked;

# checkNeighbors helper (counts unaddigned neighbors in column)
def checkCol(col, assigment):
	checked = set();
	i = 0;
	while i < 9:
		if assignment[i][col] == 0:
			checked.add((i, col));
		i += 1;
	return checked;

# checkNeighbors helper (counts unaddigned neighbors in box)
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


# checkNeighbors helper (counts unaddigned neighbors in hyperbox)
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


# val does not violate constraints
def isConsistent(val, r, c, assignment):
 	if (inRow(val, r, assignment) or 
 		inCol(val, c, assignment) or 
 		inBox(val, r, c, assignment) or 
 		inHyper(val, r, c, assignment)):
 		return False;
	return True;

# does not violate row constraint
def inRow(val, row, assignment):
	for i in range(9):
		if assignment[row][i] == val:
			return True;
	return False;

# does not violate colmumn constraint
def inCol(val, col, assignment):
	for i in range(9):
		if assignment[i][col] == val:
			return True;
	return False;


# does not violate box constraint
def inBox(val, row, col, assignment):
	tempR = (row // 3) * 3;
	tempC = (col // 3) * 3;

	i = tempR;
	while i < tempR + 3:
		j = tempC;
		while j < tempC + 3:
			if assignment[i][j] == val:
				return True;
			j += 1;
		i += 1;
	return False;


# does not violate hyperbox constraint
def inHyper(val, row, col, assignment):
	if (((row % 4) == 0) or ((col % 4) == 0)):
		return False;
	tempR = row // 4;
	tempC = col // 4;
	tempR = tempR * 4 + 1;
	tempC = tempC * 4 + 1;

	i = tempR;
	while i < tempR + 3:
		j = tempC;
		while j < tempC + 3:
			if assignment[i][j] == val:
				return True;
			j += 1
		i += 1
	return False;


# check if sudoku problem is complete
def complete(assignment):
	for row in assignment:
		for val in row:
			if val == 0:
				return False
	return True



# backtrack
def backtrack(board, assignment):
	# if its done, return True
	if complete(assignment):
		return True;
	# choosing best variable based on heuristics
	var = selectUnassigned(board, assignment); #var = (r, c) for best variable
	# test each value in var's domain
	for val in board.get(var[0], var[1]):
		# heck if hat val doesn't violate any constraints
		if isConsistent(val, var[0], var[1], assignment):
			# if it doesn't, then assign the value for that location
			assignment[var[0]][var[1]] = val;
			# and continue with rest of board
			res = backtrack(board, assignment)
			# if you can finish rest of board, return true/success
			if res == True:
				return res;
		# else it don't work, remove that assignment from the location and try the next val
			assignment[var[0]][var[1]] = 0;
	# no solution
	return False;


# printboard
def printSol(assignment):
	out = '-------------------\n|'
	row = 0;
	while row < 9:
		col = 0;
		while col < 9:
			out += str(assignment[row][col]);
			if col % 3 == 2:
				out += '|';
			else:
				out += ' ';
			col += 1;
		if row % 3 == 2:
			out += '\n-------------------';
		out += '\n|';
		row += 1;
	print(out[:-1]);


# initialize domains
board = Board('test2.txt');
#initilize assignment
assignment = [([0] * 9) for i in range(9)];

#call backtrac print soln if there is one, otherwise no solution
if backtrack(board, assignment):
	printSol(assignment)
else:
	print('no solution')
