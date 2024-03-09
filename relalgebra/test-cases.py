from functools import reduce
from predlogic2 import AND, OR, NOT, FORALL, EXISTS, ATOM, EQUAL, EQVI, IMPL, Var, Const
from relalg import RAproject, RAselect, RAtable, RAnatjoin, RAunion, RAdifference, RAdivision
import RDBMS
from RDBMS import makeTable, printTable

# Offspring data from https://en.wikipedia.org/wiki/Family_tree_of_Danish_monarchs

RELparentOf = makeTable (["PARENT","CHILD"],
                         [["Frederik","Christian"],
                          ["Frederik","Isabella"],
                          ["Frederik","Vincent"],
                          ["Frederik","Josephine"],
                          ["Mary","Christian"],
                          ["Mary","Isabella"],
                          ["Mary","Vincent"],
                          ["Mary","Josephine"],
                          ["Henrik","Frederik"],
                          ["Henrik","Joachim"],
                          ["Margrethe","Frederik"],
                          ["Margrethe","Joachim"],
                          ["Joachim","Nikolai"],
                          ["Joachim","Felix"],
                          ["Alexandra","Nikolai"],
                          ["Alexandra","Felix"],
                          ["Joachim","HenrikD"],
                          ["Joachim","Athena"],
                          ["Marie","HenrikD"],
                          ["Marie","Athena"],
                          ["Ingrid","Margrethe"],
                          ["Ingrid","Benedikte"],
                          ["Ingrid","Anne Marie"],
                          ["Frederick","Margrethe"],
                          ["Frederick","Benedikte"],
                          ["Frederick","Anne Marie"]])


RELfemale = makeTable (["PERSON"],
                       [["Isabella"],
                        ["Josephine"],
                        ["Mary"],
                        ["Margrethe"],
                        ["Alexandra"],
                        ["Athena"],
                        ["Marie"],
                        ["Ingrid"],
                        ["Benedikte"],
                        ["Anne Marie"]])

UNIVERSE = makeTable (["ELEMENT"],
                      [["Christian"],
                       ["Felix"],
                       ["Frederick"],
                       ["Frederik"],
                       ["Henrik"],
                       ["HenrikD"],
                       ["Joachim"],
                       ["Nikolai"],
                       ["Vincent"],
                       ["Alexandra"],
                       ["Anne Marie"],
                       ["Athena"],
                       ["Benedikte"],
                       ["Ingrid"],
                       ["Isabella"],
                       ["Josephine"],
                       ["Margrethe"],
                       ["Marie"],
                       ["Mary"]])

RELmale = makeTable (["PERSON"],
                     [["Frederik"],
                      ["Christian"],
                      ["Vincent"],
                      ["Henrik"],
                      ["HenrikD"],
                      ["Joachim"],
                      ["Nikolai"],
                      ["Felix"],
                      ["Frederick"]])

DENMARK = { "female" : RELfemale,
            "male" : RELmale,
            "parent" : RELparentOf,
            "U" : UNIVERSE}
DENMARKschema = { "parent" : ["PARENT","CHILD"],
                  "female" : ["PERSON"],
                  "male" : ["PERSON"],
                  "U" : ["ELEMENT"]}

###### Definitions of concepts that express family relations

# Variables, constructed from a variable name

u = Var("u")
x = Var("x")
y = Var("y")
z = Var("z")

# Python functions to express atomic formulas more compactly

female = lambda x : ATOM("female",[x])
male = lambda x : ATOM("male",[x])
mother = lambda x,y : ATOM("mother",[x,y])
father = lambda x,y : ATOM("father",[x,y])
sister = lambda x,y : ATOM("sister",[x,y])
brother = lambda x,y : ATOM("brother",[x,y])
parent = lambda x,y : ATOM("parent",[x,y])
aunt = lambda x,y : ATOM("aunt",[x,y])
uncle = lambda x,y : ATOM("uncle",[x,y])
nephew = lambda x,y : ATOM("nephew",[x,y])
grandparent = lambda x,y : ATOM("grandparent",[x,y])
grandmother = lambda x,y : ATOM("grandmother",[x,y])
sibling = lambda x,y : ATOM("sibling",[x,y])
cousin = lambda x,y : ATOM("cousin",[x,y])

# Long ANDs expressed as a list

def chainAND(l):
  if len(l) == 0:
    print("chain and of length 0")
    exit(1)
  elif len(l) == 1:
    return l[0]
  else:
   return AND(l[0],chainAND(l[1:]))

# Definitions of family relationships

# Mother, father, sister, brother, aunt, uncle, nephew, sibling, cousin
# in terms of parent, female, male

A1 = FORALL("x",FORALL("y",EQVI(mother(x,y),AND(female(x),parent(x,y)))))
A2 = FORALL("x",FORALL("y",EQVI(father(x,y),AND(male(x),parent(x,y)))))
A3 = FORALL("x",FORALL("y",EQVI(sister(x,y),AND(female(x),sibling(x,y)))))
A4 = FORALL("x",FORALL("y",EQVI(brother(x,y),AND(male(x),sibling(x,y)))))
A5 = FORALL("x",FORALL("y",EQVI(aunt(x,y),
                                AND(female(x),
                                    EXISTS("z",AND(sibling(x,z),
                                                   parent(z,y)))))))
A6 = FORALL("x",FORALL("y",EQVI(uncle(x,y),
                                AND(male(x),
                                    EXISTS("z",AND(sibling(x,z),
                                                   parent(z,y)))))))
A7 = FORALL("x",FORALL("y",EQVI(nephew(x,y),
                                AND(male(x),
                                    EXISTS("z",AND(sibling(y,z),
                                                   parent(z,x)))))))
A8 = FORALL("x",FORALL("y",EQVI(grandmother(x,y),
                                AND(female(x),
                                    grandparent(x,y)))))
A9 = FORALL("x",FORALL("y",EQVI(grandparent(x,y),
                                EXISTS("z",AND(parent(x,z),
                                               parent(z,y))))))
A10 = FORALL("x",FORALL("y",EQVI(sibling(x,y),
                                 EXISTS("z",chainAND([NOT(EQUAL(x,y)),
                                                      parent(z,x),
                                                      parent(z,y)])))))
A11 = FORALL("x",FORALL("y",EQVI(cousin(x,y),
                                 EXISTS("z",EXISTS("u",chainAND([parent(z,x),
                                                                 parent(u,y),
                                                                 sibling(z,u)]))))))

familyrelations = [A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11]

# Recognize formulas of the forma FORALL(x1,FORALL(x2, .. P(x1,...,xn) EQVI D))
# where x1,...,xn are exactly the FORALL-quantified variables, and each xi occurs
# exactly once in the atom.

def extractDef(formula):
  boundVars = set()
  while isinstance(formula,FORALL):
    boundVars.add(formula.var)
    formula = formula.subformula
  # Inside FORALL quantifiers, must have EQVI.
  if not isinstance(formula,EQVI):
    return (None,None)
  lhs = formula.subformula1
  rhs = formula.subformula2
  # The left-hand side must be an ATOM.
  if not isinstance(lhs,ATOM):
    return (None,None)
  # All terms in the ATOM must be variables
  if any(isinstance(term,Const) for term in lhs.terms):
    return (None,None)
  # The variables must be the same as in the quantifiers.
  atomVars = [ var.name for var in lhs.terms ]
  if set(atomVars) != boundVars:
    return (None,None)
  # There may not be duplicates in the variables in the atom
  if len(set(atomVars)) != len(atomVars):
    return (None,None)
  return (lhs,rhs)

# Replace non-primitive atom with its definition
# (This will not terminate if there are recursive definitions or cycles
# between two or more definitions!)

def applyDefinition(pred,terms):
  for dfn in familyrelations:
    # What does the formula 'dfn' define?
    datom,dfma = extractDef(dfn)
    if datom == None:
      return ATOM(pred,terms)
    # Defines the same predicate as in the atom?
    if datom.pred == pred:
      # Match the atom and the definition atom, creating a substitution
      subst = dict()
      for var,term in zip(datom.terms,terms):
        subst[var.name] = term
      # Function to apply the substitution to a variable, inside varMap
      def doSubst(x,boundVars):
        if x not in boundVars:
          return subst[x] # Only free variables substituted
        else:
          return Var(x)
      # Rename variables quantified in dfma2 and occurring in 'terms'
      disallow = ATOM(pred,terms).freeVars().union(dfma.freeVars())
      dfma1 = dfma.quantRename(disallow)
      # Apply the substitution to the body of the definition, and return it
      dfma2 = dfma1.varMap(doSubst,set())
      # Eliminate defined predicates also inside the definition
      return dfma2.atomMap(applyDefinition)
  return ATOM(pred,terms)

# Replace non-primitive relations by their definitions, until only primitive
# relations are left.

def reduce2primitives(formula):
  return formula.atomMap(applyDefinition)

# Show formulas and query from a database

def makeDBquery(formula,explanation,schema,DB):
  print("======= " + explanation)
  print("FORMULA: ")
  print("    " + str(formula))
  pformula = reduce2primitives(formula)
  print("FORMULA WITH DERIVED PREDICATES ELIMINATED: ")
  print("    " + str(pformula))
  RAquery = pformula.fma2RA(schema)
  print("RELATION ALGEBRA: ")
  for l in RAquery.prettyprint():
    print("  " + l)
  result = RAquery.eval(DB)
  print("QUERY RESULT:")
  printTable(result)
  print("===================================================================")

# The following tests have a free variable (usually 'x') for which possible
# values are queried from the relational database.

TESTS = [ ("Who are cousins?", cousin(x,y)),
          ("Who are male-female cousins?", AND(cousin(x,y),AND(male(x),female(y)))),
          ("Who are fathers?", EXISTS("y",father(x,y))),
          ("Who are parents of males?", EXISTS("y",AND(parent(x,y),male(y)))),
          ("Who have male cousins?", EXISTS("y",AND(cousin(x,y),male(y)))),
          ("Whose all cousins are male?", FORALL("y",IMPL(cousin(x,y),male(y)))),
          ("Whose all siblings are female?", FORALL("y",IMPL(sibling(x,y),female(y)))),
          ("Who have no siblings?", FORALL("y",NOT(sibling(x,y)))),
          ("Who have no siblings? v2", NOT(EXISTS("y",sibling(x,y)))),
          ("Who have male siblings?", EXISTS("y",AND(sibling(x,y),male(y)))),
          ("Females who have no female siblings?", AND(female(x),NOT(EXISTS("y",AND(sibling(x,y),female(y)))))),
          ("Females who have no male siblings?", AND(female(x),NOT(EXISTS("y",AND(sibling(x,y),male(y)))))),
          ("Who have a sibling who has a different parent?", EXISTS("y",AND(sibling(x,y),EXISTS("z",AND(parent(z,y),NOT(parent(z,x))))))),
          ]

if __name__ == "__main__":
  for explanation,formula in TESTS:
    makeDBquery(formula,explanation,DENMARKschema,DENMARK)
