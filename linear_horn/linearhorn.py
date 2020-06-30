# Zephaniah Hill
# The University of Michigan -- EECS 598
# June 28, 2018

from pysat.solvers import Solver, Minisat22

import numpy as np # used to generate a list of integers


class horn_clause_generator:
    def __init__(self, numb_of_variables):#, file_name):

        #self.file_name = file_name
        self.numb_of_variables = numb_of_variables + 1 # add 1 because np.arange is noninclusive.
        self.endline = ' '+str(0) # added for readability in string formatting
        horn_formula = []

    def build_using_pysat(self):
        #with open(self.filename, 'a') as f:

        var_list =  np.arange(1,self.numb_of_variables) # make a list of integers size = numb_of_variables
        horn_formula = []
        for non_neg_var in var_list: # outter loop for the non-negative variable in the horn variable
            subformula = []
            subformula.append(non_neg_var) # save the non-negative variable to the subformula
            for var in var_list: # inner loop to generate the N-1 negative variables
                if var != non_neg_var: # exlude the non-negative veriable
                    subformula.append(-var) # add each negative variable to the subformula
            horn_formula.append(subformula) # add the subformula to the horn variable
        return horn_formula # return a horn variable with all possible permutations on N variables




def main():

    variable_size_list = [10, 100, 1000] # each item in this list is used to generate a horn variable of that size
    avg_time_for_variable_size_set = [] # this list is maintained to compare the time increase per formula size
    for numb_of_variables in variable_size_list:
        linear_horn = horn_variable_generator(numb_of_variables) # instance of
        horn_formula = linear_horn.build_using_pysat() # generate a horn variable of size numb_of_variables

        avg_time = 0
        numb_runs = 10 # average the time to solve over numb_run runs of the sat solver.
        for i in range(1,numb_runs):
            with Minisat22(bootstrap_with=horn_formula, use_timer=True) as m:
                m.solve() # solve using minisat

                avg_time += m.time() # accumulate the time used in the solver
        avg_time = avg_time/numb_runs # find the real average over numb_run minisat calls
        avg_time_for_variable_size_set.append(avg_time) # maintain a list of average times for# [a, b, c]


    # this loop prints the time increase per formula
    for index, time in enumerate(avg_time_for_variable_size_set[:-1]):
        time_diff = avg_time_for_variable_size_set[index+1]/time

        print "\n" "It takes ", time_diff, " times longer to compute", variable_size_list[index+1], " variables than ", variable_size_list[index], " variables"

        #TODO: change to variables


if __name__ == '__main__':
    main()


# Example: for three varibles (variable_list_size = 3)
# Variables = [a, b, c] = [1, 2, 3]
#
# horn_clause:
# (~a + ~b + c) * (~a + b + ~c) * (a + ~b + ~c)

# horn_clauses_DIMACS:
# -1 -2 3 0
# -1 2 -3 0
# 1 -2 -3 0
