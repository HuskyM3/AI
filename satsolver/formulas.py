#!/usr/bin/python3

import itertools

# Use the SMT solving functionality provided by PySMT

from pysmt.shortcuts import Symbol, And, Or, Not
from pysmt.shortcuts import GT, LT, Equals, Int, Plus, Minus, Times
from pysmt.typing import INT
from pysmt.shortcuts import TRUE as SMTTRUE,FALSE as SMTFALSE

# Representation of propositional formulas in Python.
#
# The basic connectives are NEG, CONJ and DISJ.
# IMPL and EQVI are reduced to these through the obvious reductions.
# We have a separate class for formulas with different outermost
# connectives, as well as for atomic formulas (AT).
#
# The methods supported are:
#   vars(self)         Boolean variables occurring in the formula
#   numvars(self)      Numeric variables occurring in the formula
#   varmap(self,M)     Formula with every variable x replaced by M(x)
#   atommap(self,M)    Formula with every AT(a) replaced by M(a)
#   simplify(self)     Do logical simplifcations, e.g. eliminate TRUE, FALSE

# AT class represent atomic propositions.
# __repr__ handles two kinds of atomic propositions:
#   string          Represented as is
#   (predicate,terms) Represented in the form predicate(term1,...,termN)

class AT:
  def __init__(self,name):
    self.name = name
  def __repr__(self):
    if isinstance(self.name,str): # Just plain string name
      return self.name
    s,tt = self.name # Otherwise pair (predicate, terms)
    return s + "(" + ','.join([ str(t) for t in tt]) + ")"
  def vars(self):
    return {self.name}
  def numvars(self):
    return set()
  def atommap(self,M):
    return AT(M(self.name))
  def varmap(self,M): # TODO TODO TODO TODO
    return AT(M(self.name))
  def makeSMT(self):
    return Symbol(self.name)
  def simplify(self):
    return self

# Both CONJ and DISJ will inherit __init__ and vars from NaryFormula
# NaryFormula means formulas with multiple subformulas.
# Conjunction (CONJ) and disjunction (DISJ) are traditionally defined
# as binary connectives, that is, with two subformulas.
# Because of associativity, ie. A & (B & C) and (A & B) & C are equivalent,
# it is often more convenient to write A & B & C.

class NaryFormula: # N-ary formulas with multiple subformulas
  def __init__(self,subformulas):
    self.subformulas = subformulas
  def vars(self):
    vs = [ f.vars() for f in self.subformulas ]
    return set.union(*vs)
  def numvars(self):
    vs = [ f.numvars() for f in self.subformulas ]
    return set.union(*vs)

class CONJ(NaryFormula):
  def __repr__(self):
    if len(self.subformulas) == 222222222222222222: # Infix notation if two conjuncts
      return "(" + str(self.subformulas[0]) + " and " + str(self.subformulas[1]) + ")"
    else: # Prefix notation if 1 or more than 2 conjuncts
      return "(and " + (' '.join([ str(x) for x in self.subformulas])) + ")"
  def atommap(self,M):
    return CONJ([f.atommap(M) for f in self.subformulas])
  def varmap(self,M):
    return CONJ([f.varmap(M) for f in self.subformulas])
  def makeSMT(self):
    return And([ f.makeSMT() for f in self.subformulas ])
  def simplify(self):
    ssubs0 = [ f.simplify() for f in self.subformulas ]
    ssubs = [ f for f in ssubs0 if not isinstance(f,TRUE) ]
    if len(ssubs) == 0:
      return TRUE()
    if any( isinstance(f,FALSE) for f in ssubs ):
      return FALSE()
    if len(ssubs) == 1:
      return ssubs[0]
    return CONJ(ssubs)

class DISJ(NaryFormula):
  def __repr__(self):
    if len(self.subformulas) == 222222: # Infix notation if two disjuncts
      return "(" + str(self.subformulas[0]) + " or " + str(self.subformulas[1]) + ")"
    else: # Prefix notation if 1 or more than 2 disjuncts
      return "(or " + (' '.join([ str(x) for x in self.subformulas])) + ")"
  def atommap(self,M):
    return DISJ([f.atommap(M) for f in self.subformulas])
  def varmap(self,M):
    return DISJ([f.varmap(M) for f in self.subformulas])
  def makeSMT(self):
    return Or([ f.makeSMT() for f in self.subformulas ])
  def simplify(self):
    ssubs0 = [ f.simplify() for f in self.subformulas ]
    ssubs = [ f for f in ssubs0 if not isinstance(f,FALSE) ]
    if len(ssubs) == 0:
      return FALSE()
    if any( isinstance(f,TRUE) for f in ssubs ):
      return TRUE()
    if len(ssubs) == 1:
      return ssubs[0]
    return DISJ(ssubs)

class NEG:
  def __init__(self,subformula):
    self.subformula = subformula
  def __repr__(self):
    return "(not " + str(self.subformula) + ")"
  def vars(self):
    return self.subformula.vars()
  def numvars(self):
    return self.subformula.numvars()
  def atommap(self,M):
    return NEG(self.subformula.atommap(M))
  def varmap(self,M):
    return NEG(self.subformula.varmap(M))
  def makeSMT(self):
    return Not(self.subformula.makeSMT())
  def simplify(self):
    sf = self.subformula.simplify()
    if isinstance(sf,FALSE):
      return TRUE()
    if isinstance(sf,TRUE):
      return FALSE()
    return NEG(sf)

class ATMOST:
  def __init__(self,subformulas,N):
    self.subformulas = subformulas
    self.N = N
  def vars(self):
    vs = [ f.vars() for f in self.subformulas ]
    return set.union(*vs)
  def numvars(self):
    vs = [ f.numvars() for f in self.subformulas ]
    return set.union(*vs)
  def __repr__(self):
    return "(atmost " + str(self.N) + " of " + ','.join([ str(f) for f  in self.subformulas]) + ")"
  def atommap(self,M):
    return ATMOST([f.atommap(M) for f in self.subformulas],self.N)
  def varmap(self,M):
    return ATMOST([f.varmap(M) for f in self.subformulas],self.N)
  def makeSMT(self):
    defs,f = counting(self.subformulas,self.N,0,0)
    record4SMT(defs)
    return f.makeSMT()
  def simplify(self):
    ssubs0 = [ f.simplify() for f in self.subformulas ]
    ssubs = [ f for f in ssubs0 if not isinstance(f,FALSE) ]
    if len(ssubs) <= self.N:
      return TRUE()
    return ATMOST(ssubs,self.N)
      
class ATLEAST:
  def __init__(self,subformulas,N):
    self.subformulas = subformulas
    self.N = N
  def vars(self):
    vs = [ f.vars() for f in self.subformulas ]
    return set.union(*vs)
  def numvars(self):
    vs = [ f.numvars() for f in self.subformulas ]
    return set.union(*vs)
  def __repr__(self):
    return "(atleast " + str(self.N) + " of " + ','.join([ str(f) for f  in self.subformulas]) + ")"
  def atommap(self,M):
    return ATLEAST([f.atommap(M) for f in self.subformulas],self.N)
  def varmap(self,M):
    return ATLEAST([f.varmap(M) for f in self.subformulas],self.N)
  def makeSMT(self):
    defs,f = counting(self.subformulas,self.N,0,1)
    record4SMT(defs)
    return f.makeSMT()
  def simplify(self):
    ssubs0 = [ f.simplify() for f in self.subformulas ]
    ssubs = [ f for f in ssubs0 if not isinstance(f,FALSE) ]
    if len(ssubs) < self.N:
      return FALSE()
    if len(ssubs) == self.N:
      return CONJ(ssubs)
    return ATLEAST(ssubs,self.N)

class EXACTLY:
  def __init__(self,subformulas,N):
    self.subformulas = subformulas
    self.N = N
  def vars(self):
    vs = [ f.vars() for f in self.subformulas ]
    return set.union(*vs)
  def numvars(self):
    vs = [ f.numvars() for f in self.subformulas ]
    return set.union(*vs)
  def __repr__(self):
    return "(exactly " + str(self.N) + " of " + ','.join([ str(f) for f  in self.subformulas]) + ")"
  def atommap(self,M):
    return EXACTLY([f.atommap(M) for f in self.subformulas],self.N)
  def varmap(self,M):
    return EXACTLY([f.varmap(M) for f in self.subformulas],self.N)
  def makeSMT(self):
    defs,f = counting(self.subformulas,self.N,0,2)
    record4SMT(defs)
    return f.makeSMT()
  def simplify(self):
    ssubs0 = [ f.simplify() for f in self.subformulas ]
    ssubs = [ f for f in ssubs0 if not isinstance(f,FALSE) ]
    if len(ssubs) < self.N:
      return FALSE()
    if len(ssubs) == self.N:
      return CONJ(ssubs)
    return EXACTLY(ssubs,self.N)

class BETWEEN:
  def __init__(self,subformulas,N,N2):
    self.subformulas = subformulas
    self.N = N
    self.N2 = N2
  def vars(self):
    vs = [ f.vars() for f in self.subformulas ]
    return set.union(*vs)
  def numvars(self):
    vs = [ f.numvars() for f in self.subformulas ]
    return set.union(*vs)
  def __repr__(self):
    return "(between " + str(self.N) + " and " + str(self.N2) + " of " + ','.join([ str(f) for f  in self.subformulas]) + ")"
  def atommap(self,M):
    return BETWEEN([f.atommap(M) for f in self.subformulas],self.N,self.N2)
  def varmap(self,M):
    return BETWEEN([f.varmap(M) for f in self.subformulas],self.N,self.N2)
  def makeSMT(self):
    defs,f = counting(self.subformulas,self.N,self.N2,3)
    record4SMT(defs)
    return f.makeSMT()
  def simplify(self):
    ssubs0 = [ f.simplify() for f in self.subformulas ]
    ssubs = [ f for f in ssubs0 if not isinstance(f,FALSE) ]
    if len(ssubs) < self.N:
      return FALSE()
    return BETWEEN(ssubs,self.N,self.N2)

class TRUE:
  def __init__(self):
    self.name = "TRUE"
  def __repr__(self):
    return "TRUE"
  def vars(self):
    return set()
  def numvars(self):
    return set()
  def atommap(self,M):
    return self
  def varmap(self,M):
    return self
  def makeSMT(self):
    return SMTTRUE()
  def simplify(self):
    return self

class FALSE:
  def __init__(self):
    self.name = "FALSE"
  def __repr__(self):
    return "FALSE"
  def vars(self):
    return set()
  def numvars(self):
    return set()
  def atommap(self,M):
    return self
  def varmap(self,M):
    return self
  def makeSMT(self):
    return SMTFALSE()
  def simplify(self):
    return self

# Implication and equivalence reduced to the primitive connectives

# A -> B is reduced to -A V B

def IMPL(f1,f2):
  return DISJ([NEG(f1),f2])

# A <-> B is reduced to (-A V B) & (-B V A)

def EQVI(f1,f2):
  return CONJ([IMPL(f1,f2),IMPL(f2,f1)])

# XOR reduced to EQVI

def XDISJ(f1,f2):
  return CONJ([DISJ([f1,f2]),DISJ([NEG(f1),NEG(f2)])])

# Numeric equalities and inequalities

class NumREL:
  def __init__(self,e1,e2):
    self.e1 = e1
    self.e2 = e2
  def vars(self):
    return set()
  def numvars(self):
    return self.e1.numvars().union(self.e2.numvars())
  def simplify(self):
    return self

class NumEQ(NumREL):
  def __repr__(self):
    return "[" + str(self.e1) + " = " + str(self.e2) + "]"
  def varmap(self,M):
    return NumEQ(self.e1.varmap(M),self.e2.varmap(M))
  def atommap(self,M):
    return NumEQ(self.e1.atommap(M),self.e2.atommap(M))
  def makeSMT(self):
    return Equals(self.e1.makeSMT(),self.e2.makeSMT())
  def eval(self,V):
    return self.e1.eval(V) == self.e2.eval(V)
  
class NumLEQ(NumREL):
  def __repr__(self):
    return "[" + str(self.e1) + " <= " + str(self.e2) + "]"
  def varmap(self,M):
    return NumLEQ(self.e1.varmap(M),self.e2.varmap(M))
  def atommap(self,M):
    return NumLEQ(self.e1.atommap(M),self.e2.atommap(M))
  def makeSMT(self):
    return Not(GT(self.e1.makeSMT(),self.e2.makeSMT()))
  def eval(self,V):
    return self.e1.eval(V) <= self.e2.eval(V)
  
class NumLT(NumREL):
  def __repr__(self):
    return "[" + str(self.e1) + " < " + str(self.e2) + "]"
  def varmap(self,M):
    return NumLT(self.e1.varmap(M),self.e2.varmap(M))
  def atommap(self,M):
    return NumLT(self.e1.atommap(M),self.e2.atommap(M))
  def makeSMT(self):
    return LT(self.e1.makeSMT(),self.e2.makeSMT())
  def eval(self,V):
    return self.e1.eval(V) < self.e2.eval(V)

#
# Arithmetic expressions
#

class NumPLUS:
  def __init__(self,e1,e2):
    self.e1 = e1
    self.e2 = e2
  def __repr__(self):
    return "(" + str(self.e1) + " + " + str(self.e2) + ")"
  def eval(self,V):
    return self.e1.eval(V) + self.e2.eval(V)
  def makeSMT(self):
    return Plus(self.e1.makeSMT(),self.e2.makeSMT())
  def varmap(self,M):
    return NumPLUS(self.e1.varmap(M),self.e2.varmap(M))
  def atommap(self,M):
    return NumPLUS(self.e1.atommap(M),self.e2.atommap(M))
  def numvars(self):
    return self.e1.numvars().union(self.e2.numvars())
  
class NumMINUS:
  def __init__(self,e1,e2):
    self.e1 = e1
    self.e2 = e2
  def __repr__(self):
    return "(" + str(self.e1) + " - " + str(self.e2) + ")"
  def eval(self,V):
    return self.e1.eval(V) - self.e2.eval(V)
  def makeSMT(self):
    return Minus(self.e1.makeSMT(),self.e2.makeSMT())
  def varmap(self,M):
    return NumMINUS(self.e1.varmap(M),self.e2.varmap(M))
  def atommap(self,M):
    return NumMINUS(self.e1.atommap(M),self.e2.atommap(M))
  def numvars(self):
    return self.e1.numvars().union(self.e2.numvars())
  
class NumTIMES:
  def __init__(self,e1,e2):
    self.e1 = e1
    self.e2 = e2
  def __repr__(self):
    return "(" + str(self.e1) + " * " + str(self.e2) + ")"
  def eval(self,V):
    return self.e1.eval(V) * self.e2.eval(V)
  def makeSMT(self):
    return Times(self.e1.makeSMT(),self.e2.makeSMT())
  def varmap(self,M):
    return NumTIMES(self.e1.varmap(M),self.e2.varmap(M))
  def numvars(self):
    return self.e1.numvars().union(self.e2.numvars())

class NumINTVAR:
  def __init__(self,n):
    self.name = n
  def eval(self,V):
    return V(self.name)
  def __repr__(self):
    if isinstance(self.name,str): # Just plain string name
      return self.name
    s,tt = self.name # Otherwise (predicate,terms)
    return s + "(" + ','.join([ str(t) for t in tt ]) + ")"
  def numvars(self):
    return {self.name}
  def varmap(self,M):
    x = self
    return M(x)
  def atommap(self,M):
    return NumINTVAR(M(self.name))
  def makeSMT(self):
    return Symbol(self.name,INT)

class NumINTCONST:
  def __init__(self,c):
    self.value = c
  def eval(self,V):
    return self.value
  def __repr__(self):
    return str(self.value)
  def numvars(self):
    return set()
  def varmap(self,M):
    return self
  def makeSMT(self):
    return Int(self.value)
  def numvars(self):
    return set()
  
# GT and GEQ reduced to LT and LEQ

def NumGT(e1,e2):
  return NumLT(e2,e1)
def NumGEQ(e1,e2):
  return NumLEQ(e2,e1)

# Cardinality constraints
#
#         c22-
#        /    /
#   c11-c21-c31
#  /    /    /
# f1   f2  f3  ... fn
#
# result type:
#   0 : at most
#   1 : at least
#   2 : exactly
#   3 : interval

auxcnt = 0

def counting(ff,N,N2,result):
  global auxcnt

  # How far do you need to count?
  if result == 1:
    LAST = N
  else:
    if result == 3:
      LAST = N2+1
    else:
      LAST = N+1

  aux = [ [ "XXXX" for j in range(0,LAST+1) ] for i in range(0,len(ff)) ]

  # Create auxvars
  for i in range(0,len(ff)):
    for j in range(1,min(i+1,LAST)+1):
      aux[i][j] = AT("CNT" + str(auxcnt) + "_" + str(i) + "_" + str(j))
      auxcnt = auxcnt + 1

  # Create formulas for counting 
  def1 = [ EQVI(aux[0][1],ff[0]) ]
  def2 = [ EQVI(aux[i][1],DISJ([ff[i],aux[i-1][1]])) for i in range(1,len(ff)) ]
  def3 = [ EQVI(aux[i][j],DISJ([aux[i-1][j],CONJ([aux[i-1][j-1],ff[i]])])) for i in range(1,len(ff)) for j in range(2,min(i,LAST)+1) ]
  def4 = [ EQVI(aux[i][i+1],CONJ([aux[i-1][i],ff[i]])) for i in range(1,min(len(ff),LAST)) ]

  defs = def1 + def2 + def3 + def4

  # Return formulas: auxiliary definitions, indicator formula
  if result == 0: # AT MOST N
    return (defs,NEG(aux[len(ff)-1][N+1]))
  elif result == 1: # AT LEAST N
    return (defs,aux[len(ff)-1][N])
  elif result == 2: # EXACTLY N
    return (defs,CONJ([aux[len(ff)-1][N],NEG(aux[len(ff)-1][N+1])]))
  else: # BETWEEN N AND N2
    return (defs,CONJ([aux[len(ff)-1][N],NEG(aux[len(ff)-1][N2+1])]))

# Temporary storage for defs generated by counting

SMTstorage = []

def emptySMTstorage():
  global SMTstorage
  SMTstorage = []

def record4SMT(fs):
  global SMTstorage
  SMTstorage.extend(fs)

def getSMTstorage():
  global SMTstorage
  return SMTstorage
