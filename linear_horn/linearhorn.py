# a b c
# !a !b c
# a !b !c
# !a b !c

from pysat.solvers import Solver, Minisat22

import numpy as np # used to generate a list of integers
#p wcnf 3 6 4
#numb_var numb_clause


class Linear_horn_clause_emperically_shown:
    def __init__(self, numb_of_clauses):#, file_name):

        #self.file_name = file_name
        self.numb_of_clauses = numb_of_clauses + 1 # add 1 because np.arange is noninclusive.
        self.endline = ' '+str(0) # added for readability in string formatting
        horn_formula = []

    def generate_horn_clauses_pysat(self):
        #with open(self.filename, 'a') as f:

        var_list =  np.arange(1,self.numb_of_clauses) # make a list of integers size = numb_of_clauses
        horn_formula = []
        for non_neg_var in var_list:
            subformula = []
            subformula.append(non_neg_var)
            for var in var_list:
                if var != non_neg_var:
                    subformula.append(-var)
            horn_formula.append(subformula)
            #print(horn_formula)
        return horn_formula






def main():

    clause_size_list = [10, 100, 1000]
    avg_time_for_clause_size_set = []
    for numb_of_clauses in clause_size_list:
        #import pdb; pdb.set_trace()
        linear_horn = Linear_horn_clause_emperically_shown(numb_of_clauses)
        horn_formula = linear_horn.generate_horn_clauses_pysat()

        avg_time = 0
        numb_runs = 10
        for i in range(1,numb_runs):
            with Minisat22(bootstrap_with=horn_formula, use_timer=True) as m:
                m.solve()

                avg_time += m.time()
        avg_time = avg_time/numb_runs
        avg_time_for_clause_size_set.append(avg_time)

        print(avg_time_for_clause_size_set)

    for index, time in enumerate(avg_time_for_clause_size_set[:-1]):
        time_diff = avg_time_for_clause_size_set[index+1]/time

        print "\n" "It takes ", time_diff, " times longer to compute", clause_size_list[index+1], " clauses than ", clause_size_list[index], " clauses"

if __name__ == '__main__':
    main()




# def generate_horn_clauses_DIMACS(self):
#     with open(self.filename, 'a') as f:
#
#         var_list =  np.arange(1,self.numb_of_clauses) # make a list of integers size = numb_of_clauses
#
#         f.write(DIMACS_string_all_var_term[1:] + "\n") # add the final formula and end the line
#
#         for var in var_list:
#             DIMACS_string = ""
#             nonneg = var
#             for var in var_list:
#                 if var != nonneg:
#                     DIMACS_string += "-" + str(var) + " "
#             DIMACS_string += str(nonneg) + self.endline
#             print(DIMACS_string)
#     return horn_formula
