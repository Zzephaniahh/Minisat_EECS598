class parser(): # takes the ISCAS 89 file as input and finds all input output pairs
    def __init__(self, ISCAS_filename):
        self.filename = ISCAS_filename
        self.gate_dict = {}
        self.output_set = []
        self.input_set = []

    def get_circuit_output(self, line):
        self.output_set.append(str(re.search('\((.+?)\)', line).group(1))) # add each output to the output set.

    def get_circuit_input(self, line):
        if "INPUT" in line:
            self.input_set.append(str(re.search('\((.+?)\)', line).group(1))) # add each output to the output set.

    def get_output(self, line):
        return str(re.search('(.+?) =', line).group(1)) # save outputs as strings to a variable


    def get_gate_type(self,line):
            return str(re.search('= (.+?)\(', line).group(1)) # find each gate bounded by "= ... ("

    def get_input_set(self, line):
        found = re.search('\((.+?)\)', line).group(1) # find each input set inside brackets (x1 ... xn)
        return str(found).split(", ") # split into a list of inputs [x1, ... xn]

    def parse(self):
        file_id = open(self.filename, "r")
        lines = file_id.readlines()
        for line in lines:
            if "OUTPUT" in line:
                self.get_circuit_output(line)

            if "=" in line: # find all lines with logic gates/circuits
                output = self.get_output(line)

                gate_type = self.get_gate_type(line)

                input_set = self.get_input_set(line)

                self.gate_dict[output] = [gate_type, input_set] # save the output: {gate_Type, input_set} pair to a dict

        return self.gate_dict, self.output_set



class CNF_conversion(): # used to generate a Symbolic CNF file. An IR for use in a solver
    def __init__(self, CNF_filename, gate_dict):
        self.gate_dict = gate_dict
        self.input_set = []
        self.gate_type = ""
        self.file_name = CNF_filename
        self.output = ''
        self.file_ID = open(CNF_filename, "w")
        self.not_gate_dict = {}

    def AND(self):
        self.file_ID = open(self.file_name, "a")
        all_variable_forumula = ""
        for input in self.input_set:
        # CNF formula representing: (!f + a) * (!f + b) ...
            self.file_ID.write("(" + input + " + " + self.negate(self.output) + ")\n")
            # DIMACS string representing (f + ~a + ~b ... )
            all_variable_forumula += " + " + self.negate(input)
        self.file_ID.write("(" + self.output + all_variable_forumula + ")\n")

    def OR(self):
        self.file_ID = open(self.file_name, "a")
        all_variable_forumula = ""
        for input in self.input_set:
        # CNF formula representing: (~a + f) *(~b + f) ...
            if input in self.not_gate_dict:
                input = self.not_gate_dict[input]
            self.file_ID.write("(" + self.negate(input) + " + " + self.output + ")\n")
            # DIMACS string representing (~f + a + b ... )
            all_variable_forumula += " + " + input
        self.file_ID.write("(" + self.negate(self.output) + all_variable_forumula + ")\n")


    def XOR(self):
        self.file_ID = open(self.file_name, "a")

        all_variable_forumula = ""
        for input in self.input_set:
        # CNF formula representing: (~a + f) *(~b + f) ...
            if input in self.not_gate_dict:
                input = self.not_gate_dict[input]

            self.file_ID.write("(" + self.negate(input) + " + " + self.output + ")\n")
            # DIMACS string representing (~f + a + b ... )
            all_variable_forumula += " + " + input
        self.file_ID.write("(" + self.negate(self.output) + all_variable_forumula + ")\n")


    def NAND(self):
        self.file_ID = open(self.file_name, "a")

        all_variable_forumula = ""
        for input in self.input_set:
        # CNF formula representing: (f + a) * (f + b) ...
            if input in self.not_gate_dict:
                input = self.not_gate_dict[input]
            self.file_ID.write("(" + input + " + " + self.output + ")\n")
            # DIMACS string representing (~f + ~a + ~b ... )
            all_variable_forumula += " + " + self.negate(input)
        self.file_ID.write("(" + self.negate(self.output) + all_variable_forumula + ")\n")



    def NOR(self):
        self.file_ID = open(self.file_name, "a")
        all_variable_forumula = ""
        for input in self.input_set:
        # CNF formula representing: (~a + ~f) *(~b + ~f) ...
            if input in self.not_gate_dict:
                input = self.not_gate_dict[input]
            self.file_ID.write("(" + self.negate(input) + " + " + self.negate(self.output) + ")\n")
            # DIMACS string representing (f + a + b ... )
            all_variable_forumula += " + " + input
        self.file_ID.write("(" + self.output + all_variable_forumula + ")\n")



    def NOT(self):
        for input in self.input_set:
            self.not_gate_dict[self.output] = self.negate(input)


    def negate(self, variable):
        if "!" in variable:
            variable = variable[1:]
        else:
            variable = "!" + variable
        return variable

    def DFF(self):
        self.file_ID = open(self.file_name, "a")

        for input in self.input_set:
            if input in self.not_gate_dict:
                input = self.not_gate_dict[input]
            self.file_ID.write( self.output+ " = DFF(" + input + ")" + "\n")


    def get_cnf_from_gate(self):
        if self.gate_type == "AND":
            self.AND()
        elif self.gate_type == "OR":
            self.OR()
        elif self.gate_type == "XOR":
            self.XOR()
        elif self.gate_type == "NAND":
            self.NAND()
        elif self.gate_type == "NOR":
            self.NOR()
        elif self.gate_type == "NOT":
            self.NOT()
        elif self.gate_type == "DFF":
            self.DFF()

        else:
            print("This gate type is unsupported: " + self.gate_type)


    def gate_dict_to_cnf(self):
        with open(self.file_name) as self.file_ID:
            for self.output in self.gate_dict:
                self.gate_type = self.gate_dict[self.output][0] # Dict of the form gate_type[output] = [gate_type, input_set]
                self.input_set = self.gate_dict[self.output][1]

                self.get_cnf_from_gate()



def main():
    ###############################
    INPUT_FILE = "s208.1.isc"
    ###############################


    ###############################
    OUTPUT_FILE = "output_test.cnf"
    ###############################

    gate_dict, output_set = parser(INPUT_FILE).parse()
    file_ID = open(OUTPUT_FILE , "w")

    CNF_conversion(OUTPUT_FILE , gate_dict).gate_dict_to_cnf()

if __name__ == '__main__':
    import re # used for parsing
    import sys # used for everything
    main()


"""
 TODO:
 Add all logic functions
 MAybe a clearer way to encode DFF?
"""
