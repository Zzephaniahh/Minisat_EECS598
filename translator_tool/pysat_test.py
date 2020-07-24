
import parser # all we need to pull in the parser.
CNF_formula, var_dict = parser.cnf_parser('outputfile.cnf').parse() # can use the class like a function now.
print CNF_formula # testing functionality
print var_dict

"""
PySAT usage of CNF goes here, convert from int to variables via the dictionary.
For example:

with Minisat22(bootstrap_with=CNF_formula, use_timer=True) as m:
        SAT_Val = m.solve()
        speed = m.time()
"""
