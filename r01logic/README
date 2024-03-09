
A valuation assigns values to all of the relevant atomic formulas.
With atomic formulas A, B and C, the following are all the valuations.

A=0, B=0, C=0
A=0, B=0, C=1
A=0, B=1, C=0
A=0, B=1, C=1
A=1, B=0, C=0
A=1, B=0, C=1
A=1, B=1, C=0
A=1, B=1, C=1

These valuations can be represented in Python as follows.

v0 = []
v1 = ["C"]
v2 = ["B"]
v3 = ["B","C"]
v4 = ["A"]
v5 = ["A","C"]
v6 = ["A","B"]
v7 = ["A","B","C"]

To check if an atomic formula is true in a valuation, simply check if its name is listed in the corresponding list. This is how the function truthValue(self,v) for the class ATOM is implemented.

Let f1 = ATOM("A")
Then f1.truthValue(v1) == True  if and only if "A" in v1

The truth-values for other connectives recursively evaluate the subformulas of the formula in question, and the compute the truth-value of the formula itself. Hence for example the following holds.

Let f2 = AND(ATOM("A"),ATOM("B"))
Then f2.truthValue(v1) == True  if and only f2.subformula1.truthValue(v1) == True and f2.subformula2.truthValue(v2) == True


To test for the satisfiability of a formula F, do the following
1. Generate all valuations (this is exactly the _powerset_ of the set of all relevant atomic formulas). There is the function F.vars() to find the names of all atomic formulas in a formula.
2. Check if there is at least one valuation v such that F.truthValue(v) == True.

Similarly, for logical consequence f1 |= f2 one has to check that for _every_ valuation, either f1 is False under the valuation, or f2 is True under the valuation.

See the Python tips at https://users.aalto.fi/~rintanj1/CS-E4800/PythonHints.html for some of the operations you need in implementing the satisfiability test.

Finding all subsets of a set (represented as lists) can be done in multiple different ways. You can google for Python powerset for how to do it with Python's itertools, or you can implement a recursive function to compute a list containing all lists that corresponds to the subsets.

def powersetAsList(l):
    # The subsets of the empty set consist of the empty set only.
    if len(l) == 0:
       return [[]]
    # Otherwise consider subsets with and without an arbitrary element.
    element,*rest = l
    # All subsets without 'element'
    subsetsRest = powerset(rest)
    # All subsets with and without 'element'
    return [ [element] + subset for subset in subsetsRest ] + subsetsRest
