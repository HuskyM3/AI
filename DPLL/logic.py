#!/usr/bin/python3

import itertools


# Representation of propositional formulas in Python.
#
# The basic connectives are NOT, AND and OR.
# IMPL and EQVI are reduced to these through the obvious reductions.
# We have a separate class for formulas with different outermost
# connectives, as well as for atomic formulas (ATOM).
#
# The methods supported are:
#   negin(self)    Negation of formula; negation pushed in one level (if possible)
#   clauses(self)  Return clauses representing the formula
#   vars(self)     Return variables occurring in a formula
#


# Translation to CNF:
# Instead of applying the logical equivalences to incrementally transform
# a formula to CNF, the 'clauses' methods below perform a recursive
# transformation to sets of clauses for each formula type after
# the subformulas have been translated into clauses.
# The translations for ATOM, NOT(ATOM ...), and AND(...) are trivial.
# The complicated part is the translation for OR after its subformulas
# have been translated to clauses, i.e. computing the disjunction
# of two or more clause sets. See the accompanying Standard ML code in
# FORMULAS.sml for more explanation.

# auxiliary functions
def concatlists(ll):
    return list(itertools.chain.from_iterable(ll))


# Both AND and OR will inherit __init__ and vars from NaryFormula
# NaryFormula means formulas with multiple subformulas.
# conjunction (AND) and disjunction (OR) are traditionally defined
# as binary connectives, that is, with two subformulas.
# Because of associativity, ie. A & (B & C) and (A & B) & C are equivalent,
# it is often more convenient to write A & B & C.
class NaryFormula:  # N-ary formulas with multiple subformulas
    def __init__(self, subformulas):
        self.subformulas = subformulas

    def vars(self):
        vs = [f.vars() for f in self.subformulas]
        return set.union(*vs)


class BinaryFormula:  # Not used here
    def __init__(self, subformula1, subformula2):
        self.subformula1 = subformula1
        self.subformula2 = subformula2


# AND and OR are defined with multiple subformulas (phi1 & phi2 & ... & phiN)
class AND(NaryFormula):
    def __repr__(self):
        return "(and " + (' '.join([str(x) for x in self.subformulas])) + ")"

    def negin(self):
        return OR([NOT(f) for f in self.subformulas])

    def clauses(self):
        return concatlists([c.clauses() for c in self.subformulas])

    def is_satisfiable(self, valuation):
        sat = True
        for subformula in self.subformulas:
            sat = sat and subformula.is_satisfiable(valuation)
        return sat


class OR(NaryFormula):
    def __repr__(self):
        return "(or " + (' '.join([str(x) for x in self.subformulas])) + ")"

    def negin(self):
        return AND([NOT(f) for f in self.subformulas])

    def clauses(self):
        cclauses = [c.clauses() for c in self.subformulas]
        return [concatlists(list(c)) for c in itertools.product(*cclauses)]

    def is_satisfiable(self, valuation):
        sat = False
        for subformula in self.subformulas:
            sat = sat or subformula.is_satisfiable(valuation)
        return sat


class NOT:
    def __init__(self, subformula):
        self.subformula = subformula

    def __repr__(self):
        return "(not " + str(self.subformula) + ")"

    def negin(self):
        return self.subformula

    def clauses(self):
        if isinstance(self.subformula, ATOM):
            return [[(self.subformula.name, False)]]
        else:
            negsubformula = self.subformula.negin()
            return negsubformula.clauses()

    def vars(self):
        return self.subformula.vars()

    def is_satisfiable(self, valuation):
        return not self.subformula.is_satisfiable(valuation)


class ATOM:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def negin(self):
        return NOT(self)

    def clauses(self):
        return [[(self.name, True)]]

    def vars(self):
        return {self.name}

    def is_satisfiable(self, valuation):
        return valuation[self.name]


# Implication and equivalence reduced to the primitive connectives

# A -> B is reduced to -A V B
def IMPL(f1, f2):
    return OR([NOT(f1), f2])


# A <-> B is reduced to (-A V B) & (-B V A)
def EQVI(f1, f2):
    return AND([IMPL(f1, f2), IMPL(f2, f1)])
