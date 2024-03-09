#!/usr/bin/python3
from time import time
from dpll import dpll
from sudoku import sudoku2fma, showsudokuclues, showsudoku
import z3_wrapper


def solve_sudoku(clues):
    showsudokuclues(clues)
    formula = sudoku2fma(clues)
    variables = sorted(formula.vars())
    starting_time = time()
    clauses = formula.clauses()
    (my_result, model) = dpll({}, clauses, variables)
    my_duration = time() - starting_time
    print()
    if my_result:
        showsudoku(model)
    else:
        print("It is not solvable")
    z3_result, _, z3_duration = z3_wrapper.solve(formula)
    if z3_result != my_result:
        result = {True: "Satisfiable", False: "Unsatisfiable", None: "Unsatisfied"}
        print("Error!!! My DPLL says the problem is `{}`, but Z3 says it is `{}`".format(result[my_result],
                                                                                         result[z3_result]))
    else:
        exclamation = " Wow!" if z3_duration * 10 < my_result else ""
        print("My DPLL spent {:.3f}(s) on this, but Z3 solves it in {:.3f}(s).{}".format(my_duration,
                                                                                         z3_duration,
                                                                                         exclamation))
    print("========================================")


def main():
    print("AN EASY SUDOKU")
    # The easy ones are solved almost without search, just by performing
    # unit propagation. A little bit harder ones require from humans looking
    # ahead at the possibilities, and this means case analysis on at least
    # some of the propositional variables.
    puzzle0 = [(1, 2, 9), (1, 4, 8), (2, 5, 4), (2, 9, 5), (3, 1, 4), (3, 3, 8), (3, 4, 5), (3, 8, 9), (3, 9, 3),
               (4, 3, 9), (4, 4, 1), (4, 6, 4), (4, 7, 5), (4, 8, 7), (5, 3, 3), (5, 8, 8), (6, 3, 1), (6, 4, 9),
               (6, 6, 6), (6, 7, 3), (6, 8, 2), (7, 1, 8), (7, 3, 4), (7, 4, 3), (7, 8, 6), (7, 9, 7), (8, 5, 6),
               (8, 9, 9), (9, 2, 6), (9, 4, 2)]
    solve_sudoku(puzzle0)

    print("SUDOKU FROM LECTURE")
    puzzle1 = [(1, 3, 3), (1, 8, 4), (2, 2, 5), (2, 7, 2), (3, 4, 1), (3, 5, 8), (4, 1, 8), (4, 2, 1), (4, 3, 4),
               (5, 4, 9), (5, 6, 5), (6, 1, 6), (7, 3, 2), (7, 5, 3), (7, 6, 4), (8, 9, 1), (9, 6, 7)]
    solve_sudoku(puzzle1)

    print("ARTO INKALA'S 'WORLD'S HARDEST SUDOKU'")
    # This requires substantial search from out very simple SAT solver, and can take
    # dozens of seconds to solve.
    # (Python's implementation of hash tables are partly
    # randomized with a random number generator that get initialized with different
    # seeds on different runs), which leads our SAT solver to choose different
    # propositional variables for branching / case analysis on different runs.
    # Runtimes vary from under one second to over half a minute.)
    puzzle2 = [(1, 9, 8),
               (2, 1, 9), (2, 6, 5), (2, 7, 7),
               (3, 2, 8), (3, 3, 1), (3, 8, 3),
               (4, 2, 5), (4, 4, 1), (4, 8, 6),
               (5, 5, 4), (5, 7, 9),
               (6, 5, 5), (6, 6, 7),
               (7, 1, 4), (7, 5, 7), (7, 7, 2),
               (8, 2, 1), (8, 3, 6), (8, 4, 3), (9, 3, 8)]
    solve_sudoku(puzzle2)


if __name__ == "__main__":
    main()
