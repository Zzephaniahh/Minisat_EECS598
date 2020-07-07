# Zephaniah Hill
# The University of Michigan -- EECS 598
# June 28, 2018

class parser(): # takes the ISCAS 89 file as input and finds all input output pairs
    def __init__(self):
        self.filename = "filename here"
        self.gate_dict = {}
        self.var_to_dimac = {}
        self.dimacs_int_counter = 1

    def parse(self):#, file_id):
        file_id = open("s208.1.isc", "r")
        lines = file_id.readlines()
        for line in lines:
            if "=" in line: # find all lines with logic gates/circuits
                output = str(re.search('(.+?) =', line).group(1)) # save outputs as strings to a variable

                if output not in self.var_to_dimac: # check if the variable already has an int assigned
                    self.var_to_dimac[output] = self.dimacs_int_counter # assign an int for each unique variable
                    self.dimacs_int_counter = self.dimacs_int_counter + 1 # increase the variable count

                gate_type = str(re.search('= (.+?)\(', line).group(1)) # find each gate bounded by "= ... ("
                found = re.search('\((.+?)\)', line).group(1) # find each input set inside brackets (x1 ... xn)
                if gate_type == "NOT":
                    self.var_to_dimac[output] = -1*self.var_to_dimac[output]# needed later to encode in CNF


                input_set = str(found).split(", ") # split into a list of inputs [x1, ... xn]

                for input in input_set:
                    if input not in self.var_to_dimac: # check if the variable already has an int assigned
                        self.var_to_dimac[input] = self.dimacs_int_counter # assign an int for each unique variable
                        self.dimacs_int_counter = self.dimacs_int_counter + 1 # increase the variable count

                self.gate_dict[output] = [gate_type, input_set] # save the output: {gate_Type, input_set} pair to a dict
        return self.gate_dict, self.var_to_dimac

class gate():
    # given pairs (input_set,output) and a gate type, a CNF formul is generated and written to the file
    def __init__(self, input_set, output, var_to_dimac):
        self.input_set = input_set
        self.output = output
        self.var_to_dimac = var_to_dimac
        self.subterm = []
        self.all_var_term = []
        self.cnf_formula = []

    def AND(self):
        for input in self.input_set:
            # DIMACS CNF subformula representing: (~f + a) * (~f + b) ...
            self.subterm.append(self.var_to_dimac[input]) # appends the dimacs int for each input to the sub formula
            self.subterm.append(self.var_to_dimac[self.output]*-1) # appends the negated output
            self.cnf_formula.append(self.subterm)
            self.all_var_term.append(self.var_to_dimac[input]*-1) # add each input to the all variable subformula

            # DIMACS string representing (f + ~a + ~b ... )
        self.all_var_term.append(self.var_to_dimac[self.output])
        self.cnf_formula.append(self.all_var_term)
        return self.cnf_formula


    def OR(self):
        for input in self.input_set:
            #  DIMACS string representing: (~a + f) *(~b + f) ...
            self.subterm.append(self.var_to_dimac[input]*-1) # appends the dimacs int for each input to the sub formula
            self.subterm.append(self.var_to_dimac[self.output]) # appends the negated output
            self.cnf_formula.append(self.subterm)

            # DIMACS string representing: (~f + a + b ... )
            self.all_var_term.append(self.var_to_dimac[input]) # add each input to the all variable subformula
        self.all_var_term.append(self.var_to_dimac[self.output]*-1) # DIMACS string representing (f + ~a + ~b ... )
        self.cnf_formula.append(self.all_var_term)
        return self.cnf_formula


    def NAND(self):
        for input in self.input_set:
            #  DIMACS string representing: (a + f) *(b + f) ...
            self.subterm.append(self.var_to_dimac[input]) # appends the dimacs int for each input to the sub formula
            self.subterm.append(self.var_to_dimac[self.output]) # appends the negated output
            self.cnf_formula.append(self.subterm)

            # DIMACS string representing: (~f + ~a + ~b ... )
            self.all_var_term.append(self.var_to_dimac[input]*-1) # add each input to the all variable subformula
        self.all_var_term.append(self.var_to_dimac[self.output]*-1) # DIMACS string representing (f + ~a + ~b ... )
        self.cnf_formula.append(self.all_var_term)
        return self.cnf_formula


    def NOR(self):
        for input in self.input_set:
            #  DIMACS string representing: (~a + ~f) *(~b + ~f) ...
            self.subterm.append(self.var_to_dimac[input]*-1) # appends the dimacs int for each input to the sub formula
            self.subterm.append(self.var_to_dimac[self.output]*-1) # appends the negated output
            self.cnf_formula.append(self.subterm)

            # DIMACS string representing: (f + a + b ... )
            self.all_var_term.append(self.var_to_dimac[input]) # add each input to the all variable subformula
        self.all_var_term.append(self.var_to_dimac[self.output]) # DIMACS string representing (f + ~a + ~b ... )
        self.cnf_formula.append(self.all_var_term)
        return self.cnf_formula


class circuit(): # builds a CNF representation of the circuit from the output of the parser
    def __init__(self, gate_dict, var_to_dimac):
        self.gate_dict = gate_dict
        self.var_to_dimac = var_to_dimac
        self.cnf_for_circuit = []

    def build(self):
        #print(self.gate_dict)
        for output in self.gate_dict:

            gate_type = self.gate_dict[output][0] # gets the type from the directory

            inputs = self.gate_dict[output][1] # gets the set of inputs as a list

            current_gate = gate(inputs, output, self.var_to_dimac)
            # find gate type and build the CNF formula
            if gate_type == "AND":

                gate_cnf_formula = current_gate.AND()
                self.cnf_for_circuit += gate_cnf_formula

            elif gate_type == "OR":
                gate_cnf_formula = current_gate.OR()
                self.cnf_for_circuit += gate_cnf_formula

            elif gate_type == "NAND":
                gate_cnf_formula = current_gate.NAND()
                self.cnf_for_circuit += gate_cnf_formula

            elif gate_type == "NOR":
                gate_cnf_formula = current_gate.NOR()
                self.cnf_for_circuit += gate_cnf_formula
        return self.cnf_for_circuit


def main():
    global_label_counter = 1 # labels for DIMACS start at 1 because 0 is the endline character
    par = parser() # initalize the parser class
    gate_dict, var_to_dimac = par.parse() # use the class to get the input output pairs


    mycir = circuit(gate_dict, var_to_dimac) # instantiate the circuit class
    cnf_for_circuit = mycir.build() # use the build method to generate a DIMACS CNF representation of the input output pairs in "gate_dict"

    print(cnf_for_circuit)


if __name__ == '__main__':
    import re # used for parsing
    import sys # used for everything


    main()


    """
    TODO:
    Handle DFF and unrolling
     Add more logic functions if needed.

     """
