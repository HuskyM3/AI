#!/usr/bin/python3

# Representation of structures
#
# universe: list or set of strings (object names)
# predicates: mapping from predicate names to the corresponding sets or relations
# constants: mapping from constant names to objects
# bindings: variable bindings as used during formula evaluation
#           New bindings (from quantifiers) added with self.bind

class Structure:
  def __init__(self,universe,predicates,constants,bindings = []):
    self.universe = universe
    self.predicates = predicates
    self.constants = constants
    self.bindings = bindings
  def bind(self,id,value):
    return Structure(self.universe,self.predicates,self.constants,[ (id,value) ] + self.bindings)
  def __str__(self):
    def pred2str(p):
      return p + "{ " + ",".join([str(e) for e in self.predicates[p]]) + " } "
    return "( { " + ",".join(self.universe) + "}, " + ",".join([ pred2str(p) for p in self.predicates ]) + ", CONSTANTS)"
  
# Representation of formulas
#
# The basic connectives are NOT, AND and OR.
# IMPL and EQVI are reduced to these through the obvious reductions.
# We have a separate class for formulas with different outermost
# connectives, as well as for atomic formulas (ATOM).
#
# Both AND and OR inherit __init__ from binaryFormula

class BinaryFormula:
  def __init__(self,subformula1,subformula2):
    self.subformula1 = subformula1
    self.subformula2 = subformula2
  def freeVars(self):
    return self.subformula1.freeVars().union(self.subformula2.freeVars())
  def predSymbols(self):
    return self.subformula1.predSymbols().union(self.subformula2.predSymbols())

class AND(BinaryFormula):
  def __str__(self):
    return "(" + str(self.subformula1) + " and " + str(self.subformula2) + ")"
  def eval(self,structure):
    return self.subformula1.eval(structure) and self.subformula2.eval(structure)

class OR(BinaryFormula):
  def __str__(self):
    return "(" + str(self.subformula1) + " or " + str(self.subformula2) + ")"
  def eval(self,structure):
    return self.subformula1.eval(structure) or self.subformula2.eval(structure)

class NOT:
  def __init__(self,subformula):
    self.subformula = subformula
  def __str__(self):
    return "(not " + str(self.subformula) + ")"
  def eval(self,structure):
    return not self.subformula.eval(structure)
  def freeVars(self):
    return self.subformula.freeVars()
  def predSymbols(self):
    return self.subformula.predSymbols()

# Atomic formulas

class ATOM:
  def __init__(self,predicate,terms):
    self.pred = predicate
    self.terms = terms
  def __str__(self):
    return self.pred + "(" + ','.join([ str(t) for t in self.terms ]) + ")"
  def eval(self,structure):
    evaluatedTerms = [ t.eval(structure) for t in self.terms ]
    relation = structure.predicates[self.pred]
    return (evaluatedTerms in relation)
  def freeVars(self):
    fvs = [ t.freeVars() for t in self.terms ]
    return set.union(*fvs)
  def predSymbols(self):
    return { self.pred }

class EQUAL:
  def __init__(self,term1,term2):
    self.term1 = term1
    self.term2 = term2
  def __str__(self):
    return "(" + str(self.term1) + " = " + str(self.term2) + ")"
  def eval(self,structure):
    return self.term1.eval(structure) == self.term2.eval(structure)
  def freeVars(self):
    return self.term1.freeVars().union(self.term2.freeVars())
  def predSymbols(self):
    return set()

# Constants

class TRUE:
  def __init__(self):
    self.name = "TRUE"
  def __str__(self):
    return "TRUE"
  def eval(self,structure):
    return True
  def freeVars(self):
    return set()
  def predSymbols(self):
    return set()

class FALSE:
  def __init__(self):
    self.name = "FALSE"
  def __str__(self):
    return "FALSE"
  def eval(self,structure):
    return False
  def freeVars(self):
    return set()
  def predSymbols(self):
    return set()

# Universal and existential quantification

class FORALL:
  def __init__(self,var,subformula):
    self.var = var
    self.subformula = subformula
  def __str__(self):
    return ("forall " + self.var + " (" + str(self.subformula) + ")")
  def eval(self,structure):
    return all(self.subformula.eval(structure.bind(self.var,el)) for el in structure.universe)
  def freeVars(self):
    fvars0 = self.subformula.freeVars()
    return fvars0.difference({ self.var })
  def predSymbols(self):
    return self.subformula.predSymbols()
  
class EXISTS:
  def __init__(self,var,subformula):
    self.var = var
    self.subformula = subformula
  def __str__(self):
    return ("exists " + self.var + " (" + str(self.subformula) + ")")
  def eval(self,structure):
    return any(self.subformula.eval(structure.bind(self.var,el)) for el in structure.universe)
  def freeVars(self):
    fvars0 = self.subformula.freeVars()
    return fvars0.difference({ self.var })
  def predSymbols(self):
    return self.subformula.predSymbols()

# Terms

class Const:
  def __init__(self,name):
    self.name = name
  def __str__(self):
    return self.name
  def eval(self,structure):
    return structure.constants[self.name]
  def freeVars(self):
    return set()
  
class Var:
  def __init__(self,name):
    self.name = name
  def __str__(self):
    return self.name
  def eval(self,structure):
    for v,w in structure.bindings:
      if v==self.name:
        return w
    print("Variable " + v + " not bound")
    exit(1)
  def freeVars(self):
    return { self.name }

# Implication and equivalence reduced to the primitive connectives

# A -> B is reduced to -A V B

def IMPL(f1,f2):
  return OR(NOT(f1),f2)

# A <-> B is reduced to (-A V B) & (-B V A)

def EQVI(f1,f2):
  return AND(IMPL(f1,f2),IMPL(f2,f1))
