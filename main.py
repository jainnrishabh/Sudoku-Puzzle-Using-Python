from constraint import *

variables = {'C11': [1], 'C12': [1, 2], 'C21': [1, 2], 'C22': [1, 2]}
constraints = [
    (['C11', 'C12'], [1, 2], [2, 1]),
    (['C11', 'C21'], [1, 2], [2, 1]),
    (['C21', 'C22'], [1, 2], [2, 1]),
    (['C12', 'C22'], [1, 2], [2, 1])
]

problem = Problem()

# define variables
problem.addVariables(['C11'], [1])
problem.addVariables(['C12'], [1, 2])
problem.addVariables(['C21'], [1, 2])
problem.addVariables(['C22'], [1, 2])

# define constraints
problem.addConstraint(lambda x, y: (x, y) in [(1, 2), (2, 1)], ['C11', 'C12'])
problem.addConstraint(lambda x, y: (x, y) in [(1, 2), (2, 1)], ['C11', 'C21'])
problem.addConstraint(lambda x, y: (x, y) in [(1, 2), (2, 1)], ['C21', 'C22'])
problem.addConstraint(lambda x, y: (x, y) in [(1, 2), (2, 1)], ['C12', 'C22'])

solutions = problem.getSolutions()

print(solutions)


# variables = {'C11': [1], 'C12': [1, 2], 'C21': [1, 2], 'C22': [1, 2]}
# constraints = [
#     (['C11', 'C12'], [1, 2], [2, 1]),
#     (['C11', 'C21'], [1, 2], [2, 1]),
#     (['C21', 'C22'], [1, 2], [2, 1]),
#     (['C12', 'C22'], [1, 2], [2, 1])
# ]