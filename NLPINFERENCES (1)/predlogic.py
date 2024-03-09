#!/usr/bin/python3

# Representation of formulas in Python.
#
# The basic connectives are NOT, AND and OR.
# IMPL and EQVI are reduced to these through the obvious reductions.
# We have a separate class for formulas with different outermost
# connectives, as well as for atomic formulas (ATOM).
#

# Both AND and OR inherit __init__ from binaryFormula
# NaryFormula means formulas with multiple subformulas.

class BinaryFormula: # Not used here
  def __init__(self,subformula1,subformula2):
    self.subformula1 = subformula1
    self.subformula2 = subformula2

class AND(BinaryFormula):
  def __str__(self):
    return "(" + str(self.subformula1) + " and " + str(self.subformula2) + ")"
  def TPTP(self):
    return "(" + self.subformula1.TPTP() + " & " + self.subformula2.TPTP() + ")"

class OR(BinaryFormula):
  def __str__(self):
    return "(" + str(self.subformula1) + " or " + str(self.subformula2) + ")"
  def TPTP(self):
    return "(" + self.subformula1.TPTP() + " | " + self.subformula2.TPTP() + ")"

class NOT:
  def __init__(self,subformula):
    self.subformula = subformula
  def __str__(self):
    return "(not " + str(self.subformula) + ")"
  def TPTP(self):
    return "~ " + self.subformula.TPTP()

# Atomic formulas

class ATOM:
  def __init__(self,predicate,terms):
    self.pred = predicate
    self.terms = terms
  def __str__(self):
    return self.pred + "(" + ','.join([ str(t) for t in self.terms ]) + ")"
  def TPTP(self):
    return self.pred + "(" + ','.join([ t.TPTP() for t in self.terms ]) + ")"

class EQUAL:
  def __init__(self,term1,term2):
    self.term1 = term1
    self.term2 = term2
  def __str__(self):
    return "(" + str(self.term1) + " = " + str(self.term2) + ")"
  def TPTP(self):
    return "(" + self.term1.TPTP() + " = " + self.term2.TPTP() + ")"

# Constants

class TRUE:
  def __init__(self):
    self.name = "TRUE"
  def __str__(self):
    return "TRUE"

class FALSE:
  def __init__(self):
    self.name = "FALSE"
  def __str__(self):
    return "FALSE"

# Universal quantification

class FORALL:
  def __init__(self,var,subformula):
    self.var = var
    self.subformula = subformula
  def __str__(self):
    return ("forall " + self.var + " " + str(self.subformula))
  def TPTP(self):
    return ("! [" + self.var.upper() + "] : " + self.subformula.TPTP())
  
class EXISTS:
  def __init__(self,var,subformula):
    self.var = var
    self.subformula = subformula
  def __str__(self):
    return ("exists " + self.var + " " + str(self.subformula))
  def TPTP(self):
    return ("? [" + self.var.upper() + "] : " + self.subformula.TPTP())

# Terms

class Const:
  def __init__(self,name):
    self.name = name
  def __str__(self):
    return self.name
  def TPTP(self):
    return self.name.lower()
  
class Var:
  def __init__(self,name):
    self.name = name
  def __str__(self):
    return self.name
  def TPTP(self):
    return self.name.upper()

# Implication and equivalence reduced to the primitive connectives

# A -> B is reduced to -A V B

def IMPL(f1,f2):
  return OR(NOT(f1),f2)

# A <-> B is reduced to (-A V B) & (-B V A)

def EQVI(f1,f2):
  return AND(IMPL(f1,f2),IMPL(f2,f1))
