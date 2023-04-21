import queue
from data import * 
from copy import deepcopy
from sudoku_constraints_9X9 import constraints

#Part 1 - 9X9 Values and CSP Class
def getCellValues(A, B):
    return ["C" + a + b for a in A for b in B]

def getUnitsList():	
	return ([getCellValues("123456789", c) for c in "123456789"] +
            			 [getCellValues(r, "123456789") for r in "123456789"] +
            			 [getCellValues(rs, cs) for rs in ('123','456','789') for cs in ('123','456','789')])

class csp:
	def __init__ (self, domain = "123456789", grid = ""):
		self.variables = getCellValues("123456789", "123456789")
		self.domain = self.getDict(grid)
		self.values = self.getDict(grid)
		self.unitlist = getUnitsList()
		self.units = dict((s, [u for u in self.unitlist if s in u]) for s in getCellValues("123456789", "123456789"))
		self.neighbors = dict((s, set(sum(self.units[s],[]))-set([s])) for s in getCellValues("123456789", "123456789"))
		self.constraints = constraints 
		self.assignments = []

	
	def getDict(self, grid=""):
		i = 0
		values = dict()
		for cell in self.variables:
			if grid[i]!='0':
				values[cell] = grid[i]
			else:
				values[cell] = "123456789"
			i = i + 1
		return values
	

#--------------------------------------------------------------------------------------------------------------------------------------
#Part 2 
#Revise function that takes CSP as per part 1 mentioned earlier and names of two variables as input 	
def Revise(csp, Xi, Xj):
	# default value as false
	revised = False
	# set of values in domain Xi  
	values = set(csp.values[Xi])

	# check for each value of domain Xi 
	for x in values:
		# if value is not inconsistent
		if not isconsistent(csp, x, Xi, Xj):
			# remove value from domain Xi
			csp.values[Xi] = csp.values[Xi].replace(x, '')
			# return true if any are removed 
			revised = True 

	# return false if any are removed 
	return revised 

# function to check if a value is inconsistent 
def isconsistent(csp, x, Xi, Xj):
	# for each value of domain Xj
	for y in csp.values[Xj]:
		# we check neighbour and constraints 
		if csp.constraints.get((Xi, Xj)) is not None:
			# return true if inconsistent 
			if Xj in csp.neighbors[Xi] and ([int(x),int(y)] in csp.constraints.get((Xi, Xj))):
				return True
		elif csp.constraints.get((Xj, Xi)) is not None:
			if Xj in csp.neighbors[Xi] and ([int(x),int(y)] in csp.constraints.get((Xj, Xi))):
				return True
	return False

#--------------------------------------------------------------------------------------------------------------------------------------
# Part 3 
# AC-3 as a function which takes as input a CSP and modifies it such that any incon- sistent values agetCellValues all domains are removed.
def AC3(csp):                                           # function AC-3(csp) returns false if an inconsistency is found and true otherwise
	q = queue.Queue()                                   # queue ← a queue of arcs, initially all the arcs in csp
	for arc in csp.constraints:
		q.put(arc)
	
	while not q.empty():                                # while queue is not empty do
		(Xi, Xj) = q.get()                              # (Xi, Xj )← POP(queue)
		if Revise(csp, Xi, Xj):                         # if REVISE(csp, Xi, Xj) then
			if len(csp.values[Xi]) == 0:                # if size of Di = 0 
				return False                            # then return false

			for Xk in (csp.neighbors[Xi] - set(Xj)):    # for each Xk in Xi.NEIGHBORS - {Xj} do
				q.put((Xk, Xi))                         # add (Xk, Xi) to queue

	return True                                         # return true

#--------------------------------------------------------------------------------------------------------------------------------------
#Part 4
def minimumRemainingValues(assignment, csp):
	unassigned_variables = dict((squares, len(csp.values[squares])) for squares in csp.values if squares not in assignment.keys())
	mrv = min(unassigned_variables, key=unassigned_variables.get)
	return mrv

#--------------------------------------------------------------------------------------------------------------------------------------
#PART 5 
def Backtracking_Search(csp):                                       # function BACKTRACKING-SEARCH(csp) returns a solution or failure
	return Backtrack({}, csp)                                       # return BACKTRACK(csp, { })


def Backtrack(assignment, csp):                                     # function BACKTRACK(csp, assignment) returns a solution or failure        
	csp.assignments.append(deepcopy(assignment))
	if set(assignment.keys())==set(getCellValues("123456789", "123456789")):  # if assignment is complete then 
		return assignment											# return assignment
	var = minimumRemainingValues(assignment, csp)					# var ← SELECT-UNASSIGNED-VARIABLE(csp, assignment)
	domain = deepcopy(csp.values)
	for value in csp.values[var]:                                   # for each value in ORDER-DOMAIN-VALUES(csp, var , assignment) do
		if isValueConsitent(var, value, assignment, csp):               # if value is consistent with assignment then
			assignment[var] = value                                 # add {var = value} to assignment
			inferences = {}
			inferences = Inference(assignment, inferences, csp, var, value)     # inferences ← INFERENCE(csp, var , assignment)
			if inferences!= "FAILURE":                              # if inferences = failure then
				result = Backtrack(assignment, csp)                 # result ← BACKTRACK(csp, assignment)
				if result!="FAILURE":                               # if result = failure then return result
					return result

			del assignment[var]                                     # remove inferences from csp
			csp.values.update(domain)                               # remove {var = value} from assignment
	return "FAILURE"                                                # return failure

def isValueConsitent(var, value, assignment, csp):
	for neighbor in csp.neighbors[var]:
		if neighbor in assignment.keys() and assignment[neighbor]==value:
			return False
	return True

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

sudoku = csp(grid='000006080300002700705100600009400000080090020000008300004007805002800006050900000')

if(AC3(sudoku)):
	result = Backtracking_Search(sudoku)

print(result)

