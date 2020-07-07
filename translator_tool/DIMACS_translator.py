# Zephaniah Hill
# The University of Michigan -- EECS 598
# June 28, 2018

class parser(): # takes the ISCAS 89 file as input and finds all input output pairs
    def __init__(self):
        self.filename = "filename here"
        self.gate_dict = {}

    def parse(self):#, file_id):
        file_id = open("s208.1.isc", "r")
        lines = file_id.readlines()
        for line in lines:
            if "=" in line: # find all lines with logic gates/circuits
                output = str(re.search('(.+?) =', line).group(1)) # save outputs as strings to a variable
                gate_type = str(re.search('= (.+?)\(', line).group(1)) # find each gate bounded by "= ... ("
                found = re.search('\((.+?)\)', line).group(1) # find each input set inside brackets (x1 ... xn)
                if gate_type == "NOT":
                    output = "NEGATE" + output
                #import pdb; pdb.set_trace()
                input_set = str(found).split(", ") # split into a list of inputs [x1, ... xn]
                self.gate_dict[output] = [gate_type, input_set] # save the output: {gate_Type, input_set} pair to a dict
        return self.gate_dict


class gate():
    # given pairs (input_set,output) and a gate type, a CNF formul is generated and written to the file
    def __init__(self, inputs, global_label_counter, file_name, variable_to_DIMACS_int_dict):
        self.inputs = inputs
        self.global_label_counter = global_label_counter # need to maintain a global counter so minisat always makes a new variable for a new input
        self.endline = ' '+str(0) # space 0 to end the line
        self.filename = file_name
        self.variable_to_DIMACS_int_dict = variable_to_DIMACS_int_dict


    def AND(self):
        with open(self.filename, 'a') as f:
            DIMACS_string_subterm = ""
            DIMACS_string_all_var_term = ""


            output_str = str(self.global_label_counter) # allocate one space for the output
            self.global_label_counter = self.global_label_counter + 1

            for input in self.inputs:
                if input not in self.variable_to_DIMACS_int_dict: # make sure only generate a new DIMACS int for unique each variable
                    input_str = str(self.global_label_counter)
                    self.global_label_counter = self.global_label_counter + 1
                    self.variable_to_DIMACS_int_dict[input] = input_str

                else:
                    input_str = self.variable_to_DIMACS_int_dict[input]

                # DIMACS string representing: (~f + a) * (~f + b) ...
                DIMACS_string_subterm = "-" + input_str + " " +  output_str + self.endline
                f.write(DIMACS_string_subterm + "\n") # each sub formula is added to the file
                # DIMACS string representing (f + ~a + ~b ... )
                DIMACS_string_all_var_term = DIMACS_string_all_var_term + " -" + input_str
            DIMACS_string_all_var_term = DIMACS_string_all_var_term + " " + output_str + self.endline
            f.write(DIMACS_string_all_var_term[1:] + "\n") # add the final formula and end the line
            return self.global_label_counter

    def OR(self):
        with open(self.filename, 'a') as f:

            DIMACS_string_subterm = ""
            DIMACS_string_all_var_term = ""

            output_str = str(self.global_label_counter) # allocate one space for the output
            self.global_label_counter = self.global_label_counter + 1

            for input in self.inputs:
                input_str = str(self.global_label_counter)
                self.global_label_counter = self.global_label_counter + 1
                #  DIMACS string representing: (~a + f) *(~b + f) ...
                DIMACS_string_subterm =  "-"  + input_str + " " +  output_str + self.endline
                f.write(DIMACS_string_subterm[1:] + "\n") # each sub formula is added to the file

                # DIMACS string representing: (~f + a + b ... )
                DIMACS_string_all_var_term = DIMACS_string_all_var_term + " " + input_str
            DIMACS_string_all_var_term = DIMACS_string_all_var_term + " -" + output_str + self.endline
            f.write(DIMACS_string_all_var_term[1:] + "\n") # add the final formula and end the line
            return self.global_label_counter


    def NAND(self):
        with open(self.filename, 'a') as f:

            DIMACS_string_subterm = ""
            DIMACS_string_all_var_term = ""

            output_str = str(self.global_label_counter) # allocate one space for the output
            self.global_label_counter = self.global_label_counter + 1

            for input in self.inputs:
                input_str = str(self.global_label_counter)
                self.global_label_counter = self.global_label_counter + 1
                #  DIMACS string representing: (a + f) *(b + f) ...
                DIMACS_string_subterm = input_str + " " +  output_str + self.endline
                f.write(DIMACS_string_subterm + "\n") # each sub formula is added to the file

                # DIMACS string representing: (~f + ~a + ~b ... )
                DIMACS_string_all_var_term = DIMACS_string_all_var_term + " " + "-"+ input_str
            DIMACS_string_all_var_term = DIMACS_string_all_var_term + "-" + output_str + self.endline
            f.write(DIMACS_string_all_var_term[1:] + "\n") # add the final formula and end the line
            return self.global_label_counter

    def NOR(self):
        with open(self.filename, 'a') as f:
            #import pdb; pdb.set_trace()

            DIMACS_string_subterm = ""
            DIMACS_string_all_var_term = ""

            output_str = str(self.global_label_counter) # allocate one space for the output
            self.global_label_counter = self.global_label_counter + 1

            for input in self.inputs:
                input_str = str(self.global_label_counter)
                self.global_label_counter = self.global_label_counter + 1
                #  DIMACS string representing: (~a + ~f) *(~b + ~f) ...
                DIMACS_string_subterm = "-" + input_str + " -" +  output_str + self.endline
                f.write(DIMACS_string_subterm + "\n") # each sub formula is added to the file
                # DIMACS string representing: (f + a + b ... )
                DIMACS_string_all_var_term = DIMACS_string_all_var_term  + " -"+ input_str
            DIMACS_string_all_var_term = DIMACS_string_all_var_term + " " + output_str + self.endline
            f.write(DIMACS_string_all_var_term[1:] + "\n") # add the final formula and end the line
            return self.global_label_counter


class circuit(): # builds a CNF representation of the circuit from the output of the parser
    def __init__(self, gate_dict, global_label_counter, file_name):
        self.gate_dict = gate_dict
        self.global_label_counter = global_label_counter
        self.file_name = file_name
        self.variable_to_DIMACS_int_dict = {}

    def build(self):
        print(self.gate_dict)
        for output in self.gate_dict:

            gate_type = self.gate_dict[output][0] # gets the type from the directory

            inputs = self.gate_dict[output][1] # gets the set of inputs as a list

            self.variable_to_DIMACS_int_dict[output] = self.global_label_counter

            current_gate = gate(inputs, self.global_label_counter, self.file_name, self.variable_to_DIMACS_int_dict)
            # find gate type and build the CNF formula
            if gate_type == "AND":
                 # note, there's no need to pass output because all gates have 1 output, and outputs are unique
                 # Is this true? ^ maybe not wise because an output may be listed as an input prior to the output def.
                 # I think I should add a dict: var dict[var_name] = {var_integer} to check this.
                 # so the counter is simply incremented by 1.
                self.global_label_counter = current_gate.AND()

            elif gate_type == "OR":
                self.global_label_counter = current_gate.OR()

            elif gate_type == "NAND":
                self.global_label_counter = current_gate.NAND()

            elif gate_type == "NOR":
                self.global_label_counter = current_gate.NOR()


def main():
    global_label_counter = 1 # labels for DIMACS start at 1 because 0 is the endline character
    par = parser() # initalize the parser class
    gate_dict = par.parse() # use the class to get the input output pairs

    file_name = "test.txt" # the file which the DIMACS formula will be written to

    mycir = circuit(gate_dict, global_label_counter, file_name) # instantiate the circuit class
    mycir.build() # use the build method to generate a DIMACS CNF representation of the input output pairs in "gate_dict"



if __name__ == '__main__':
    import re # used for parsing
    import sys # used for everything


    main()


    """
    TODO:
     Add more logic functions if needed.
     Handle NOT cases.
     Add initializing line.
     Add the ability to unroll.
     Check variable integer to name mapping using dict.
     """
