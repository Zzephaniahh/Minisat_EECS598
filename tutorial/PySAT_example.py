# Zephaniah Hill
# The University of Michigan -- EECS 598
# July 2, 2018


from pysat.solvers import Solver, Minisat22 # import the needed libraries

# The formula we solve using minisat is:
# (x+y+z)*(!x+!y+!z)
# to encode these we define an integer for each variable
# {x = 1, y = 2, z = 3}
# The structure is a list of lists, where each sublist is a subformula which is ANDed to the other items in the superlist.
# (x+y+z) = [1, 2, 3]
# (!x+!y+!z) = [-1, -2, -3] the negation operator is signified by a negative integer.
CNF_formula = [[1,2,3],[1,2,3]]

with Minisat22(bootstrap_with=CNF_formula, use_timer=True) as m:
    print(m.solve()) # solve using minisat

    print(m.time())
