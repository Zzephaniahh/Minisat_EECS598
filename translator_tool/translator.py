# global counter to track used integers
# the gate dict will be of the form: {output, {inputs}}
import time

class parser():
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
                #import pdb; pdb.set_trace()
                input_set = str(found).split(", ") # split into a list of inputs [x1, ... xn]
                self.gate_dict[output] = [gate_type, input_set] # save the output: {gate_Type, input_set} pair to a dict
        return self.gate_dict


class gate():
    def __init__(self, inputs, global_label_counter, file_name):
        self.inputs = inputs
        self.global_label_counter = global_label_counter
        self.endline = ' '+str(0) # space 0 to end the line
        self.filename = file_name


    def AND(self): # we want (~out+in_i)*(~[in_i]+out)
        with open(self.filename, 'a') as f:
            DIMACS_string_subterm = ""
            DIMACS_string_all_var_term = ""

            output_str = str(self.global_label_counter) # allocate one space for the output
            self.global_label_counter = self.global_label_counter + 1

            for input in self.inputs:
                input_str = str(self.global_label_counter)
                self.global_label_counter = self.global_label_counter + 1
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



class circuit():
    def __init__(self, gate_dict, global_label_counter, file_name):
        self.gate_dict = gate_dict
        self.global_label_counter = global_label_counter
        self.file_name = file_name

    def build(self):
        for output in self.gate_dict:

            gate_type = self.gate_dict[output][0] # gets the type from the directory

            inputs = self.gate_dict[output][1] # gets the set of inputs as a list
            current_gate = gate(inputs, self.global_label_counter, self.file_name)
            # find gate type and build the CNF formula
            if gate_type == "AND":
                 # note, there's no need to pass output because all gates have 1 output
                 # so the counter is simply incremented by 1.
                self.global_label_counter = current_gate.AND()

            elif gate_type == "OR":
                self.global_label_counter = current_gate.OR()

            elif gate_type == "NAND":
                self.global_label_counter = current_gate.NAND()

            elif gate_type == "NOR":
                self.global_label_counter = current_gate.NOR()






def main():
    global_label_counter = 1
    par = parser()
    gate_dict = par.parse()
    file_name = "test.txt"
    mycir = circuit(gate_dict, global_label_counter, file_name)
    mycir.build()



if __name__ == '__main__':
    import re
    import sys


    main()
