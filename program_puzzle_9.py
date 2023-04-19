import queue
from data import * 
from copy import deepcopy
from sudoku_constraints import constraints

#Part 1

digits =  cols = "123456789"
rows = "123456789"

def cross(A, B):
	return ["C" + a + b for a in A for b in B]

squares = cross(rows, cols)

class csp:
	def __init__ (self, domain = digits, grid = ""):
		self.variables = squares
		self.domain = self.getDict(grid)
		self.values = self.getDict(grid)
				
		self.unitlist = ([cross(rows, c) for c in cols] +
            			 [cross(r, cols) for r in rows] +
            			 [cross(rs, cs) for rs in ('123','456','789') for cs in ('123','456','789')])

		self.units = dict((s, [u for u in self.unitlist if s in u]) for s in squares)
		
		self.neighbors = dict((s, set(sum(self.units[s],[]))-set([s])) for s in squares)
		self.constraints = constraints 
		self.assignments = []
		# self.constraints = {(variable, peer) for variable in self.variables for peer in self.neighbors[variable]}

	
	def getDict(self, grid=""):
		i = 0
		values = dict()
		for cell in self.variables:
			if grid[i]!='0':
				values[cell] = grid[i]
			else:
				values[cell] = digits
			i = i + 1
		return values
	

#--------------------------------------------------------------------------------------------------------------------------------------
#Part 2 	
def Revise(csp, Xi, Xj):
	revised = False
	values = set(csp.values[Xi])

	for x in values:
		if not isconsistent(csp, x, Xi, Xj):
			csp.values[Xi] = csp.values[Xi].replace(x, '')
			revised = True 

	return revised 

def isconsistent(csp, x, Xi, Xj):
	for y in csp.values[Xj]:
		if csp.constraints.get((Xi, Xj)) is not None:
			if Xj in csp.neighbors[Xi] and ([int(x),int(y)] in csp.constraints.get((Xi, Xj))):
				return True
		elif csp.constraints.get((Xj, Xi)) is not None:
			if Xj in csp.neighbors[Xi] and ([int(x),int(y)] in csp.constraints.get((Xj, Xi))):
				return True
	return False

#--------------------------------------------------------------------------------------------------------------------------------------
# Part 3 
def AC3(csp):
	q = queue.Queue()

	for arc in csp.constraints:
		q.put(arc)
	
	i = 0
	while not q.empty():
		(Xi, Xj) = q.get()
		i = i + 1 

		if Revise(csp, Xi, Xj):
			if len(csp.values[Xi]) == 0:
				return False

			for Xk in (csp.neighbors[Xi] - set(Xj)):
				q.put((Xk, Xi))

	return True 

#--------------------------------------------------------------------------------------------------------------------------------------
#Part 4

def Select_Unassigned_Variables(assignment, csp):
	unassigned_variables = dict((squares, len(csp.values[squares])) for squares in csp.values if squares not in assignment.keys())
	mrv = min(unassigned_variables, key=unassigned_variables.get)
	return mrv
# print(Select_Unassigned_Variables({'C11': '1', 'C12': '1234', 'C13': '1234', 'C14': '1234', 'C21': '1234', 'C22': '2', 'C23': '1234', 'C24': '1234', 'C31': '1234', 'C32': '1234', 'C33': '3', 'C34': '1234', 'C41': '1234', 'C42': '1234' } , sudoku))

#PART 5 

#BACKTRACKING SEARCH INITIALIZES THE INITIAL ASSIGNMENT AND CALLS THE BACKTRACK FUNCTION
def Backtracking_Search(csp):
	return Backtrack({}, csp)



#THE RECURSIVE FUNCTION WHICH ASSIGNS VALUE USING BACKTRACKING 
def Backtrack(assignment, csp):
	csp.assignments.append(assignment)
	if set(assignment.keys())==set(squares):
		return assignment

	var = Select_Unassigned_Variables(assignment, csp)
	domain = deepcopy(csp.values)

	for value in csp.values[var]:
		if isConsistent(var, value, assignment, csp):
			assignment[var] = value
			inferences = {}
			inferences = Inference(assignment, inferences, csp, var, value)
			result = Backtrack(assignment, csp)
			if result!="FAILURE":
				return result
			del assignment[var]
			csp.values.update(domain)
			

	return "FAILURE"



#CHECKS IF THE GIVEN NEW ASSIGNMENT IS CONSISTENT
def isConsistent(var, value, assignment, csp):
	for neighbor in csp.neighbors[var]:
		if neighbor in assignment.keys() and assignment[neighbor]==value:
			return False
	return True

#FORWARD CHECKING USING THE CONCEPT OF INFERENCES
def Inference(assignment, inferences, csp, var, value):
	inferences[var] = value

	for neighbor in csp.neighbors[var]:
		if neighbor not in assignment and value in csp.values[neighbor]:
			if len(csp.values[neighbor])==1:
				return "FAILURE"

			remaining = csp.values[neighbor] = csp.values[neighbor].replace(value, "")

			if len(remaining)==1:
				flag = Inference(assignment, inferences, csp, neighbor, remaining)
				if flag=="FAILURE":
					return "FAILURE"

	return inferences



sudoku = csp(grid='700400086051080400040307090309006100000020000004900708080102060006050910210003005')

solved  = Backtracking_Search(sudoku) 

print(sudoku.assignments)
