#!/usr/bin/python3

from predlogic import *
from stparse import parseStructFile
from prparse import parseFormulaFile

# Evaluate formulas w.r.t. a given structure

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: predlogic [structure file] [formula file]")
        exit(1)
    else:
        structFilename = sys.argv[1]
        formulaFilename = sys.argv[2]
    universe,predicates,predicate_arities,constants = parseStructFile(structFilename)
    print("==== Structure file: " + structFilename + " done ==========")
    structure = Structure(universe,predicates,constants)
    formulas = parseFormulaFile(formulaFilename,predicate_arities,constants)
    print("==== Formula file: " + formulaFilename + " done ==========")
    print("=====================================================================")
    print("Universe: " + " ,".join(structure.universe))
    for P in predicates:
        relation = predicates[P]
        arity = predicate_arities[P]
        print("Predicate '" + P + "' with arity " + str(arity))
        for e in relation:
            print("    " + str(e))
    for C in constants:
        print("Constant " + C + " = " + constants[C])
    print("=====================================================================")
    for f in formulas:
        if f.eval(structure) == True:
            print("TRUE  : " + str(f))
        else:
            print("FALSE : " + str(f))
    print("=====================================================================")
