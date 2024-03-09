#!/usr/bin/python3

import time
import sys
from qfparser import parseinputfile, LogicSyntaxError, LogicLexerError
from formulas import getSMTstorage, testSatisfiability, trueVariables

def main():
    if len(sys.argv) != 2:
        print("Must give exactly one argument [file]")
        exit(1)
    args = sys.argv
    filename = args[1]
    print("Input file: " + filename)
    try:
        gformulas,allvars = parseinputfile(filename)
    except LogicSyntaxError:
        print("SYNTAX ERROR")
        exit(1)
    except LogicLexerError:
        print("LEXICAL ERROR")
        exit(1)
    print("VARIABLES: " + ' '.join(sorted(allvars)))
    print("INTERMEDIATE REPRESENTATION:")
    for f in gformulas:
        print(str(f))
    print("Translating to SMT")
    ALLSMT = [ f.makeSMT() for f in gformulas ] + [ f.makeSMT() for f in getSMTstorage() ]
    print("Calling SAT solver")
    start = time.time()
    assignment = testSatisfiability(ALLSMT)
    end = time.time()
    if assignment:
        print("SAT")
        trueVars = trueVariables(assignment,allvars)
        for x in allvars:
            if x in trueVars:
                print(x + " := 1")
            else:
                print(x + " := 0")
    else:
        print("UNSAT: Not satisfiable")
    print("Solver runtime: %.2f" % (end-start))

main()
