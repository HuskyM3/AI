#!/usr/bin/python3

import itertools

# Representation of propositional formulas in Python.
#
# The basic connectives are NOT, AND and OR.
# IMPL and EQVI are reduced to these through the obvious equivalences.
# Separate classes represent each connective, atomic formulas, and
# the constants TRUE and FALSE.
#
# The methods supported are:
#   f.vars(self)          Set of all variables occurring in the formula f
#   f.truthValue(self,v)  Compute truth-value of f under valuation 'v'
#                         Returns True if v |= f and False otherwise
#
# Valuations are represented as sets/lists consisting of the names
# of those atomic formulas that are True. For example, the empty
# set/list corresponds to the valuation in which all atomic formulas
# are False. To test if the formula ATOM("a") is true in a valuation
# V, one tests if "a" is an element of the set/list V.

# Superclass to handle parts of AND and OR

class BinaryFormula:
  def __init__(self,subformula1,subformula2):
    self.subformula1 = subformula1
    self.subformula2 = subformula2
  def vars(self):
    return self.subformula1.vars().union(self.subformula2.vars())

# Both AND and OR will inherit __init__ and vars from BinaryFormula

# AND - conjunction

class AND(BinaryFormula):
  def __repr__(self):
    return "(" + str(self.subformula1) + " AND " + str(self.subformula2) + ")"
  def truthValue(self,v):
### IMPLEMENT THIS (~ 1 line)
    #print(self.vars())
    #print(self.vars().issubset(v))
    return self.subformula1.truthValue(v) and self.subformula2.truthValue(v)
# OR - disjunction

class OR(BinaryFormula):
  def __repr__(self):
    return "(" + str(self.subformula1) + " OR " + str(self.subformula2) + ")"
  def truthValue(self,v):
### IMPLEMENT THIS (~ 1 line)
    return self.subformula1.truthValue(v) or self.subformula2.truthValue(v) #not self.vars().isdisjoint(v) and not len(v) == 0
# NOT - negation

class NOT:
  def __init__(self,subformula):
    self.subformula = subformula
  def __repr__(self):
    return "(NOT " + str(self.subformula) + ")"
  def vars(self):
    return self.subformula.vars()
  def truthValue(self,v):
### IMPLEMENT THIS (~ 1 line)
      return not self.subformula.truthValue(v)
# ATOM - atomic formulas

class ATOM:
  def __init__(self,name):
    self.name = name
  def __repr__(self):
    return self.name
  def vars(self):
    return {self.name}
  def truthValue(self,v):
### IMPLEMENT THIS (~ 1 line)
    return self.vars().issubset(v)

# FALSE - the constant that represents the truth-value False

class FALSE:
  def __repr__(self):
    return "FALSE"
  def vars(self):
    return set()
  def truthValue(self,v):
### IMPLEMENT THIS (~ 1 line)
    return False
# TRUE - the constant that represents the truth-value True

class TRUE:
  def __repr__(self):
    return "TRUE"
  def vars(self):
    return set()
  def truthValue(self,v):
### IMPLEMENT THIS (~ 1 line)
    return True


# Implication and equivalence reduced to the primitive connectives

# A -> B is reduced to -A V B

def IMPL(f1,f2):
  return OR(NOT(f1),f2)

# A <-> B is reduced to (A -> B) & (B -> A)

def EQVI(f1,f2):
  return AND(IMPL(f1,f2),IMPL(f2,f1))

# Test for the satisfiability of a formula
# This function should return False if the formula is unsatisfiable,
# and otherwise it will return a valuation that satisfies the formula.
# The valuation is a list of names of true atomic formulas.

# A very simple implementation would first find the set of all
# variables occurring in a formula, and then generate all possible
# subsets of that set (or corresponding lists), which represent
# all possible valuations, and then test if the given formula is
# true in at least one of the valuations.

# 'satisfiable' returns False if the formula is NOT satisfiable,
# and it returns the valuation that makes the formula true otherwise.

def satisfiable(f):
### IMPLEMENT THIS (10 to 15 lines total)
    #print(f.truthValue())
    #f[0]
    
    input_set = f.vars()
    #print(EQVI(list(input_set)[0], list(input_set)[1]).truthValue(input_set))
    sorted_input_tuple = tuple(sorted(input_set))
    n = len(sorted_input_tuple)
    all_subsets = []
    for subset_size in range(0, n + 1):
        subsets = itertools.combinations(sorted_input_tuple, subset_size)
        all_subsets.extend(list(subsets))
    a =  [set(subset) for subset in all_subsets]
    #print(a)
    #print(f)
    for i in a:
      #print(f.truthValue(i))
      if(f.truthValue(i)):
        #print(i)
        return i
    return False
# Test logical consequence
# Returns True if f2 is a logical consequence of f1 (that is f1 |= f2)
# and returns False otherwise.

def logicalConsequence(f1,f2):
### IMPLEMENT THIS (~ 1 line
  #a = (satisfiable(f2))
  #b = (satisfiable(f1))
  print(satisfiable(f1))
  print(satisfiable(f2))
  #print(satisfiable(IMPL(f2, f1)))
  #print(satisfiable(IMPL(f1, f2)))
  #print(satisfiable(EQVI(f2, f1)))
  #print(satisfiable(EQVI(f1, f2)))
  #print(satisfiable(f2).issubset(satisfiable(f1)))
  #print(IMPL(a, b))
  return satisfiable(f2).issubset(satisfiable(f1)) #or satisfiable(IMPL(f2, f1))