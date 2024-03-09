
from pysmt.typing import INT
from pysmt.shortcuts import get_model
from pysmt.shortcuts import And

import sys
from fparser import parseinputfile, LogicSyntaxError, LogicLexerError
from formulas import getSMTstorage, Symbol

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
    print("PROPOSITIONAL LOGIC TRANSLATION:")
    for f in gformulas:
        print(str(f))
    ALLSMT = And([ f.makeSMT() for f in gformulas ] + [ f.makeSMT() for f in getSMTstorage() ])
    assignment = get_model(ALLSMT)
    if assignment:
        print("SAT")
        for x in allvars:
            if assignment.get_py_value(Symbol(x)) == True:
                print(x + " := 1")
            else:
                print(x + " := 0")
#        print(assignment)
    else:
        print("UNSAT: Not satisfiable")

main()
