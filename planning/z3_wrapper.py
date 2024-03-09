from time import time
from typing import List, Tuple
from logic import AND, OR, NOT, ATOM
from z3 import Solver, Bool, BoolRef, And, Or, Not, sat


def literal_conversion(literal: Tuple[str, bool]) -> BoolRef:
    if literal[1]:
        return Bool(literal[0])
    else:
        return Not(Bool(literal[0]))


def clause_conversion(clause: List[Tuple[str, bool]]) -> BoolRef:
    return Or(*[literal_conversion(literal) for literal in clause])


def formula_conversion(formula) -> BoolRef:
    if isinstance(formula, ATOM):
        return Bool(formula.name) 
    if isinstance(formula, NOT):
        return Not(formula_conversion(formula.subformula))
    if isinstance(formula, OR):
        return Or(*[formula_conversion(f) for f in formula.subformulas])
    if isinstance(formula, AND):
        return And(*[formula_conversion(f) for f in formula.subformulas])
    print("Error: the given formula is not a logical object")

def solve(formula) -> Tuple[bool, List, float]:
    z3_formula = formula_conversion(formula)
    solver = Solver()
    starting_time = time()
    solver.append(z3_formula)
    result = solver.check()
    if (result==sat):
        m = solver.model()
    else:
        m = {}
    ending_time = time()
    return result == sat, m, ending_time - starting_time
