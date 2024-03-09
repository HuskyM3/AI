#!/usr/bin/python3

from logic import AND, OR, NOT, ATOM

def at_least_one(formulas):
    return OR(formulas)

def all_pairs(lst):
  return [ (lst[i],lst[j]) for i in range(0,len(lst)) for j in range(i+1,len(lst)) ]

def at_most_one(formulas):
    return AND([NOT(AND([f1, f2])) for (f1, f2) in all_pairs(formulas)])

def exactly_one(formulas):
    return AND([at_most_one(formulas), at_least_one(formulas)])

# Translation of Sudoku to propositional logic

def create_variable_name(column, row, number):
    return str(column) + "," + str(row) + "," + str(number)


def variable(column, row, number):
    return ATOM(create_variable_name(column, row, number))


# Map 9X9 Sudoku instances to propositional formulas
#
# In formulas C1 to C4 below, instead of exactly1 it would be logically
# equivalent to use OR. However, the exactly1 allows Unit Propagation in DPLL
# to infer far more new literals, and cutting down the size of the search tree
# to a small fraction. In fact, our simple SAT solver needs at least a couple
# of hours (and possibly far far longer: these runs did not finish before we
# terminated them after 2 hours) to solve even simple instances if there is
# OR instead of exactly1 in these formulas.

def sudoku2fma(puzzle):
    # Every grid cell has exactly one value
    C1 = AND([exactly_one([variable(c, r, n) for n in range(1, 10)]) for r in range(1, 10) for c in range(1, 10)])

    # Every row has all numbers
    C2 = AND([exactly_one([variable(c, r, n) for c in range(1, 10)]) for r in range(1, 10) for n in range(1, 10)])

    # Every column has all numbers
    C3 = AND([exactly_one([variable(c, r, n) for r in range(1, 10)]) for c in range(1, 10) for n in range(1, 10)])

    # Every 3X3 sub-grid has all numbers
    C4 = AND(
        [exactly_one([variable(c + dc, r + dr, n) for dr in range(0, 3) for dc in range(0, 3)]) for c in range(1, 8, 3)
         for r in range(1, 8, 3) for n in range(1, 10)])

    # The solution respects the given clues
    C5 = AND([variable(x, y, n) for (x, y, n) in puzzle])

    return AND([C1, C2, C3, C4, C5])


# Output a satisfying valuation for Sudoku as a 9X9 grid

def showsudokuclues(clues):
    for y in range(9, 0, -1):
        for x in range(1, 10):
            flag = False
            for n in range(1, 10):
                if (x, y, n) in clues:
                    print(str(n), end='')
                    flag = True
            if not flag:
                print(".", end='')
            if x in [3, 6]:
                print("|", end='')
        print("")
        if y in [7, 4]:
            print("===|===|===")


def showsudoku(V):
    for y in range(9, 0, -1):
        for x in range(1, 10):
            for n in range(1, 10):
                if V[create_variable_name(x, y, n)]:
                    print(str(n), end='')
            if x in [3, 6]:
                print("|", end='')
        print("")
        if y in [7, 4]:
            print("-----------")
