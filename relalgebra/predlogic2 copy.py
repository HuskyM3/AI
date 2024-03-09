#!/usr/bin/python3

from functools import reduce
from relalg import RAproject, RAselect, RAtable, RAnatjoin, RAunion, RAdifference, RAdivision, RArename
from RDBMS import cNot, cAnd, cOr, cEQ, cCOL, cCONST

# Representation of predicate logic formulas
#
# The basic connectives are NOT, AND, OR and EQVI. IMPL is reduced to NOT and OR.
# Other classes for formulas are ATOM, EXISTS, FORALL, and EQUAL.
#
# The methods are:
#
#   atomMap(self,f) for replacing every atom x in a formula by f(x)
#
#   varMap(self,f,bv) for replacing every variable x by f(x,bv)
#      Here bv will contain all variables bound by surrounding quantifiers
#      (so that bounds and free variables can be distinguished.)
#
#   fma2RA(self,dbSchema) for translating a formula to Relational Algebra
#      dbSchema contains names of the columns for each relation in the DB
#
#   quantRename(self,disallowed) renames quantified variables to avoid clashes
#      when replacing a derived predicate with its definition when the latter
#      quantifies variables that occur in the atom. Here 'disallowed' is the
#      variables that should be renamed to avoid incorrect quantification.


class BinaryFormula:
    def __init__(self,subformula1,subformula2):
        self.subformula1 = subformula1
        self.subformula2 = subformula2

    def freeVars(self):
        return self.subformula1.freeVars().union(self.subformula2.freeVars())

    def quantRename(self,disallowed):
        cls = type(self)
        return cls(self.subformula1.quantRename(disallowed),self.subformula2.quantRename(disallowed))

# The Conjunction AND
# AND is directly translated to the Natural Join in the relational algebra,
# but some of the optimizations for EQUAL and NOT are possible when
# they are inside a conjunction. This is separated to 'optimizeANDfma2RA'.

class AND(BinaryFormula):
    def __str__(self):
        return "(" + str(self.subformula1) + " and " + str(self.subformula2) + ")"
    def __eq__(self,other):
        if isinstance(other,AND):
            if(self.subformula1 == other.subformula1 and self.subformula2 == other.subformula2):
                return True
        return False

    # Map function for atoms
    def atomMap(self,f):
        return AND(self.subformula1.atomMap(f),self.subformula2.atomMap(f))

    # Map function for variables (to variables and terms)
    def varMap(self,f,bv):
        return AND(self.subformula1.varMap(f,bv),self.subformula2.varMap(f,bv))

    # Translation of AND is to Natural Join in the relational algebra.
    def fma2RA(self,dbSchema):
        # See if there are opportunities to optimize.
        result = optimizedANDfma2RA(self.subformula1,self.subformula2,dbSchema)
        if result != None:
            return result
        # Something else: use the generic translation.
        return RAnatjoin(self.subformula1.fma2RA(dbSchema),self.subformula2.fma2RA(dbSchema))

# Optimize the translation of EQUAL and NOT when a part of AND.
# PHI AND (t1=t2) translates to a select with condition t1=t2.
# PHI AND NOT PHI' translates to relational difference.

def optimizedANDfma2RA(subformula1,subformula2,dbSchema):
    # Good formulas are ones translatable to relational algebra "easily"
    def good(formula):
        if isinstance(formula,ATOM):
            return True
        if isinstance(formula,AND) and (good(formula.subformula1) or good(formula.subformula2)):
            return True
        if isinstance(formula,OR) and good(formula.subformula1) and good(formula.subformula2):
            return True
        if isinstance(formula,EQVI) and good(formula.subformula1) and good(formula.subformula2):
            return True
        if isinstance(formula,FORALL) and good(formula.subformula):
            return True
        if isinstance(formula,EXISTS) and good(formula.subformula):
            return True
        return False

    # See if exactly one conjunct is 'good'
    if good(subformula1) and not good(subformula2):
        goodformula = subformula1
        badformula = subformula2
    elif good(subformula2) and not good(subformula1):
        goodformula = subformula2
        badformula = subformula1
    else:
        # Both or neither conjunct is good: Use the generic translation.
        return None

    # The bad conjunct is NOT PHI. Use relational difference.
    if isinstance(badformula,NOT) and good(badformula.subformula):
        if goodformula.freeVars() == badformula.freeVars():
            # To be able to use difference, the free variables (columns)
            # have to be the same
            #print(goodformula.fma2RA(dbSchema))
            return RAdifference(goodformula.fma2RA(dbSchema),badformula.subformula.fma2RA(dbSchema))
        else:
            return None
    # Map logic terms (constants and variables) to DB constants and columns
    def term2dbterm(term):
        if isinstance(term,Const):
            return cCONST(term.value)
        if isinstance(term,Var):
            return cCOL(term.name)
    # The bad conjunct is an equality. Use relational select.
    if isinstance(badformula,EQUAL) and badformula.freeVars().issubset(goodformula.freeVars()):
        return RAselect(cEQ(term2dbterm(badformula.term1),term2dbterm(badformula.term2)),goodformula.fma2RA(dbSchema))
    # The bad conjunct is a negated equality. Use relational select.
    if isinstance(badformula,NOT) and isinstance(badformula.subformula,EQUAL) and badformula.freeVars().issubset(goodformula.freeVars()):
        return RAselect(cNot(cEQ(term2dbterm(badformula.subformula.term1),term2dbterm(badformula.subformula.term2))),goodformula.fma2RA(dbSchema))
    return None

# The Disjunction OR

class OR(BinaryFormula):
    def __str__(self):
        return "(" + str(self.subformula1) + " or " + str(self.subformula2) + ")"
    def __eq__(self,other):
        if isinstance(other,OR):
            if self.subformula1 == other.subformula1 and self.subformula2 == other.subformula2:
                return True
        return False

    # Map function for atoms
    def atomMap(self,f):
        return OR(self.subformula1.atomMap(f),self.subformula2.atomMap(f))

    # Map function for variables (to variables and terms)
    def varMap(self,f,bv):
        return OR(self.subformula1.varMap(f,bv),self.subformula2.varMap(f,bv))

    # OR translates to relational union, but union's both tables must have
    # the same columns. To make sure they have, conjuncts for the
    # universal relation U may have to be added.
    def fma2RA(self,dbSchema):
        # Variables in the two disjuncts
        vars1 = self.subformula1.freeVars()
        vars2 = self.subformula2.freeVars()
        # Which vars to add?
        varsToAdd1 = vars2.difference(vars1)
        varsToAdd2 = vars1.difference(vars2)
        # Add U(x) as a conjunct for every missing variable
        fixedSubformula1 = reduce(AND,[ ATOM("U",[Var(x)]) for x in varsToAdd1],self.subformula1)
        fixedSubformula2 = reduce(AND,[ ATOM("U",[Var(x)]) for x in varsToAdd2],self.subformula2)
        # Union of the tables obtained from the two disjuncts
        return RAunion(fixedSubformula1.fma2RA(dbSchema),fixedSubformula2.fma2RA(dbSchema))

class EQVI(BinaryFormula):
    def __str__(self):
        return "(" + str(self.subformula1) + " eqvi " + str(self.subformula2) + ")"
    def __eq__(self,other):
        if isinstance(other,EQVI):
            if self.subformula1 == other.subformula1 and self.subformula2 == other.subformula2:
                return True
        return False

    # Map function for atoms
    def atomMap(self,f):
        return EQVI(self.subformula1.atomMap(f),self.subformula2.atomMap(f))

    # Map function for variables (to variables and terms)
    def varMap(self,f,bv):
        return EQVI(self.subformula1.varMap(f,bv),self.subformula2.varMap(f,bv))

    def fma2RA(self,dbSchema):
        # Reduce equivalence to other connectives, and translate the result.
        f = AND(IMPL(self.subformula1,self.subformula2),IMPL(self.subformula2,self.subformula1))
        return f.fma2RA(dbSchema)

class NOT:
    def __init__(self,subformula):
        self.subformula = subformula
    def __str__(self):
        return "(not " + str(self.subformula) + ")"
    def __eq__(self,other):
        if isinstance(other,NOT):
            if self.subformula == other.subformula:
                return True
        return False
    def freeVars(self):
        return self.subformula.freeVars()

    # Map function for atoms
    def atomMap(self,f):
        return NOT(self.subformula.atomMap(f))

    # Map function for variables (to variables and terms)
    def varMap(self,f,bv):
        return NOT(self.subformula.varMap(f,bv))

    # Negation translates to a difference from (a Cartesian product of)
    # the universal relation U so that the relational difference is for tables
    # with the same columns.
    def fma2RA(self,dbSchema):
        # Variables in the two disjuncts
        #print(dbSchema)
        #vars1 = self.freeVars()
        #vars2 = self.subformula.freeVars()
        # Which vars to add?
        #print(self.subformula)
        #a = self.freeVars().difference(self.subformula.freeVars())
        #print(self.freeVars())
        #print(self.subformula.freeVars())
        #varsToAdd1 = vars2.difference(vars1
        # kaikki 
        #varsToAdd2 = vars1.difference(vars2)
        # Add U(x) as a conjunct for every missing variable

        # otetaan kaikki atomit jotka on olemassa 
        # loop lista läpi jossa on kaikki atomit 
        # subformulan freevars pitää tehdä jotain jotta voi poistaa 
        

        def fma2RA(self, dbSchema):
            mi = reduce(
                AND,
                [ATOM("U", [Var(x)]) for x in self.subformula.freeVars()],
            )
            wtf = RAdifference(
                mi.fma2RA(dbSchema),
                self.subformula.fma2RA(dbSchema),
            )
            return wtf

           #second = reduce(AND,[ ATOM("U",[Var(col)]) for col in self.subformula.freeVars() if col != self.subformula.freeVars()])
            #print(second)
            #second = { col for col in self.subformula.freeVars() if col != self.var}
            # miten second pitäisi tehdä? 
            # pitäisi olla kaikki jutut siinä
            # en ole ihan varma mitkä kaikki osat kuuluvat siihen? 
            # ne pitäsi tulla self.subformula.freeVars() 
            #print(self.var)
        #fixedSubformula1 = reduce(AND,[ ATOM("U",[Var(x)]) for x in varsToAdd1],self)
        #fixedSubformula2 = reduce(AND,[ ATOM("U",[Var(x)]) for x in varsToAdd2],self.subformula)
        # Union of the tables obtained from the two disjuncts
        # atoms and subformulas freevars 
        # if col != self.subformula.freeVars() if col != self.subformula.freeVars()
        print(type(self.subformula.fma2RA(dbSchema)))
        second = reduce(AND,[ ATOM("U",[Var(col)]) for col in self.subformula.freeVars()])
        #print(second)
        ## käytännössä AND lisätään jokaiseen atomiin
        

        #print(self.subformula.fma2RA(dbSchema))
        return RAdifference(second.fma2RA(dbSchema), self.subformula.fma2RA(dbSchema) )        
        #print(self.subformula.freeVars())
         #RAunion(fixedSubf ormula1.fma2RA(dbSchema),fixedSubformula2.fma2RA(dbSchema))
        # might need some subformulas 
        # basically second should be the one which is excluded 
        # is there need for tables to be same like in the eqvi?
        # unnion example 
  
###### IMPLEMENT THIS
###### IMPLEMENT THIS
        

    # Rename some of the quantified variables.
    def quantRename(self,disallowed):
        return NOT(self.subformula.quantRename(disallowed))

# Atomic formulas

class ATOM:
    def __init__(self,predicate,terms):
        self.pred = predicate
        self.terms = terms
    def __str__(self):
        return self.pred + "(" + ','.join([ str(t) for t in self.terms ]) + ")"
    def __eq__(self,other):
        if isinstance(other,ATOM):
            if self.pred == other.pred and len(self.terms) == len(other.terms):
                for (t1,t2) in zip(self.terms,other.terms):
                    if not(t1 == t2):
                        return False
                return True
        return False
    def freeVars(self):
        l = [ t.freeVars() for t in self.terms ]
        return set.union(*l)

    # Map function for atoms
    def atomMap(self,f):
        return f(self.pred,self.terms)

    # Map function for variables (to variables and terms)
    def varMap(self,f,bv):
        def mapTerm(t):
            if isinstance(t,Var) and t.name not in bv:
                return f(t.name,bv)
            else:
                return t
        return ATOM(self.pred,[ mapTerm(t) for t in self.terms ])

    # Atoms correspond to reading a DB table, possibly with selection and projection,
    # and column names replaced by names of variables in the atom.
    # See course material for details of this translation.
    def fma2RA(self,dbSchema):
        # Match table's column names with the terms in the atom.
        columns = list(zip(dbSchema[self.pred],self.terms))
        # Which columns have a constant in the atom?
        constantCols = [ (col,term) for (col,term) in columns if isinstance(term,Const) ]
        # Which columns have a variable in the atom?
        varCols = [ (col,term) for (col,term) in columns if not isinstance(term,Const) ]
        # The table for the predicate.
        ra0 = RAtable(self.pred)
        # Needs to do a SELECT if some terms are constants.
        if len(constantCols) == 0:
            ra1 = ra0
        else:
            # Select rows where the column value matches the constant.
            ra1a = RAselect(functools.reduce(cAnd,[ cEQ(cCOL(col),cCONST(term.value)) for (col,term) in constantCols]),ra0)
            # Keep the non-constant columns, which correspond to variables.
            ra1 = RAproject({ col for (col,term) in varCols},ra1a)
        # Rename the columns to the variable names.
        renaming = dict()
        for col,term in varCols:
            renaming[col] = term.name
        ra2 = RArename(renaming,ra1)
        return ra2
    # Rename some of the quantified variables.
    def quantRename(self,disallowed):
        return self

class EQUAL:
    def __init__(self,term1,term2):
        self.term1 = term1
        self.term2 = term2
    def __str__(self):
        return "(" + str(self.term1) + " = " + str(self.term2) + ")"
    def __eq__(self,other):
        if isinstance(other,EQUAL):
            if self.term1 == other.term1 and self.term2 == other.term2:
                return True
        return False

    def atomMap(self,f):
        return self

    def varMap(self,f,bv):
        def mapTerm(t):
            if isinstance(t,Var):
                return f(t.name,bv)
            else:
                return t
        return EQUAL(mapTerm(self.term1),mapTerm(self.term2))

    def freeVars(self):
        return self.term1.freeVars().union(self.term2.freeVars())

    # Translation of equality (without being a conjunct in a nice conjunction)
    # is a bit inefficient, as it may require relations with almost all
    # elements in the universe.
    def fma2RA(self,dbSchema):
        fv = self.freeVars()
        # Translate predicate logic terms to RDBMS column and value references.
        def PLterm2RAterm(term):
            if isinstance(term,Const):
                return cCONST(term.value)
            if isinstance(term,Var):
                return cCOL(term.name)
            return None
        # One U-table for every variable term in the equality.
        tables = [ RArename({"ELEMENT" : v },RAtable("U")) for v in fv ]
        # Join the U tables and select rows that satisfy the equality.
        return RAselect(cEQ(PLterm2RAterm(self.term1),PLterm2RAterm(self.term2)),reduce(RAnatjoin,tables))
    # Rename some of the quantified variables.
    def quantRename(self,disallowed):
        return self

# Helper function to rename quantified variables in quantRename
#
#   disallowed   Variables that should not be quantified in the subformula
#   var          Variable that is to be renamed to something else
#   subformula   Subformula where that variable possibly occurs free
#
# Generate a new variable name which does not occur in 'disallowed'.
# Replace free occurrences of 'var' in 'subformula' by 'newvar', producing 'newsubformula'.
# Return (newvar,newsubformula)

def fixQuantification(disallowed,var,subformula):
    # Pool of candidate variable names
    candidates = [ base + index for index in ["","1","2","3","4","5","6","7","8"] for base in ["x","y","z","u","v","w"]]
    # Find a variable name that does not occur in 'disallowed'.
    newvar = None
    for w in candidates:
        if w not in disallowed:
            newvar = w
            break
    if newvar == None:
        print("Could not find an unused variable")
        exit(1)
    # Function to map free occurrences of 'var' to 'newvar'
    def f(x,boundVars):
        if x != var or x in boundVars:
            return Var(x)
        else:
            return Var(newvar)
    # Replace free occurrences of 'var' by 'newvar'.
    newsubformula = subformula.varMap(f,set())
    # Return the results.
    return (newvar,newsubformula)

# Universal quantification

class FORALL:
    def __init__(self,var,subformula):
        self.var = var
        self.subformula = subformula
    def __str__(self):
        return ("forall " + self.var + " " + str(self.subformula))
    def __eq__(self,other):
        if isinstance(other,FORALL):
            if self.subformula == other.subformula and self.var == other.var:
                return True
        return False

    # Free variables of A X.P are free variables of P minus { X }
    def freeVars(self):
        return self.subformula.freeVars().difference( { self.var } )

    def atomMap(self,f):
        return FORALL(self.var,self.subformula.atomMap(f))

    def varMap(self,f,bv):
        return FORALL(self.var,self.subformula.varMap(f,bv.union({self.var})))

    # Translation to relational algebra by relational division
    def fma2RA(self,dbschema):
        if self.var not in self.subformula.freeVars():
            # Variable does not occur in the formula. Ignore quantifier.
            return self.subformula.fma2RA(dbschema)
        else: 
            #RAunion(fixedSubformula1.fma2RA(dbSchema),fixedSubformula2.fma2RA(dbSchema))
            ## might need some subformulas like or
            #doesn't have subformula since not binaryformula? 
            # what should be divided? 
            # basically second should be the one which is not wanted 
            #second = {col for col in self.subformula.freeVars() if col == self.var}
            #print(dbschema)
            # 
            # second pitää sisällään ne atomit joista halutaan jakaa pois ne jotka ovat myös 
            #print(self.var)
            # mitä tarvitaan 
            # eiks käytännössä vaan kaikki mahdolliset atomit jotka sitten poistetaan 
            #second = { col for col in self.subformula.freeVars() if col == self.var}
            second = reduce(AND,[ ATOM("U",[Var(col)]) for col in self.subformula.freeVars() if col != self.var])
            #second = reduce(AND,[ ATOM("U",[Var(col)]) for col in self.subformula.freeVars()])
            #second = { col for col in self.freeVars() }
            #print(second)
            #print(self.subformula.fma2RA(dbschema))
            #print(self.subformula)
            #print(self.subformula)
            return RAdivision(second.fma2RA(dbschema), self.subformula.fma2RA(dbschema))
###### IMPLEMENT THIS
###### IMPLEMENT THIS

    def quantRename(self,disallowed):
        if self.var not in disallowed:
            return FORALL(self.var,self.subformula.quantRename(disallowed))
        else:
            newvar,newsubformula = fixQuantification(disallowed,self.var,self.subformula)
            return FORALL(newvar,newsubformula.quantRename(disallowed.union({newvar})))
  
class EXISTS:
    def __init__(self,var,subformula):
        self.var = var
        self.subformula = subformula
    def __str__(self):
        return ("exists " + self.var + " " + str(self.subformula))
    def __eq__(self,other):
        if isinstance(other,EXISTS):
            if self.subformula == other.subformula and self.var == other.var:
                return True
        return False

    # Free variables of E X.P are free variables of P minus { X }
    def freeVars(self):
        return self.subformula.freeVars().difference( { self.var } )

    def atomMap(self,f):
        return EXISTS(self.var,self.subformula.atomMap(f))

    def varMap(self,f,bv):
        return EXISTS(self.var,self.subformula.varMap(f,bv.union({self.var})))

    # Translation to relational algebra by projection
    def fma2RA(self,dbSchema):
        return RAproject({ col for col in self.subformula.freeVars() if col != self.var},self.subformula.fma2RA(dbSchema))

    def quantRename(self,disallowed):
        if self.var not in disallowed:
            return EXISTS(self.var,self.subformula.quantRename(disallowed))
        else:
            newvar,newsubformula = fixQuantification(disallowed,self.var,self.subformula)
            return EXISTS(newvar,newsubformula.quantRename(disallowed.union({newvar})))

# Terms

class Const:
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return self.value
    def __eq__(self,other):
        if isinstance(other,Const) and self.value == other.value:
            return True
        return False
    def freeVars(self):
        return set()
  
class Var:
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return self.name
    def __eq__(self,other):
        if isinstance(other,Var) and self.name == other.name:
            return True
        return False
    def freeVars(self):
        return { self.name }

# Implication and equivalence reduced to the primitive connectives

# A -> B is reduced to -A V B

def IMPL(f1,f2):
  return OR(NOT(f1),f2)
