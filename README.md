There are currently three seprate projects in this directory.

1 -- Full Adder:
  Directory:
    full_adder

  This is an excercise that goes along with my Minisat tutorial PDF. The two files are identical, except the "error" version has one gate flipped.

2 -- Horn Clause Linearity:
  Directory:
    linear_horn

  This python file generates and profiles varying sizes of horn formulas using minisat through a python API (pysat). It shows that while SAT is NP generally, special case (horn) can be solved in linear time.

3 -- Translator Tool:
  Directory:
    translator_tool

  This tool reads in a netlist in the ISCAS 89 format, and translates it to CNF DIMACS format, then prints it to a file. This tool is partially finished. 
