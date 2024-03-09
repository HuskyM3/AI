#!/usr/bin/python3

# Representation of propositional formulas in Python.
#
# The basic connectives are NOT, AND and OR.
# IMPL and EQVI are reduced to these through the obvious reductions.
# We have a separate class for formulas with different outermost
# connectives, as well as for atomic formulas (ATOM).
#
# The method 'map' constructs a new copy of a formula with
# the name N of every atomic formula replaced by f(N).

# Both AND and OR will inherit __init__ from NaryFormula
# NaryFormula means formulas with multiple subformulas.
# conjunction (AND) and disjunction (OR) are traditionally defined
# as binary connectives, that is, with two subformulas.
# Because of associativity, ie. A & (B & C) and (A & B) & C are equivalent,
# it is often more convenient to write A & B & C.

class NaryFormula:  # N-ary formulas with multiple subformulas
    def __init__(self, subformulas):
        self.subformulas = subformulas

class AND(NaryFormula):
    def __repr__(self):
        return "(and " + (' '.join([str(x) for x in self.subformulas])) + ")"
    def map(self,f):
        return AND([ c.map(f) for c in self.subformulas])

class OR(NaryFormula):
    def __repr__(self):
        return "(or " + (' '.join([str(x) for x in self.subformulas])) + ")"
    def map(self,f):
        return OR([ d.map(f) for d in self.subformulas])

class NOT:
    def __init__(self, subformula):
        self.subformula = subformula
    def __repr__(self):
        return "(not " + str(self.subformula) + ")"
    def map(self,f):
        return NOT(self.subformula.map(f))

class ATOM:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        s,n = self.name
        return s + "@" + str(n)
    def map(self,f):
        return ATOM(f(self.name))

# Implication and equivalence reduced to the primitive connectives

# A -> B is reduced to -A V B

def IMPL(f1, f2):
    return OR([NOT(f1), f2])

# A <-> B is reduced to (-A V B) & (-B V A)

def EQVI(f1, f2):
    return AND([IMPL(f1, f2), IMPL(f2, f1)])
