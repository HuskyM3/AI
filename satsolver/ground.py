
#
# Grounding of parametric transition definitions
#

from formulas import *

# Given a transition system, ground it, and translate into
# a set of formulas in the propositional logic.

# Instantiate a term for given variable bindings
# Terms are either
#   variables referred to in the bindings
#   alphanumeric constants
#   numeric expressions that refer to variables in the bindings

def instantiateterm(t,bindings):
    for e in bindings:
        k,v = e
        if k==t:
            return str(v) # It is a bound variable
    if isinstance(t,str): # It is a constant symbol
        return t
    # Otherwise it is a numeric expression
    def V(x):
        for e in bindings:
            k,v = e
            if k==x:
                return v # It is a bound variable
        return x # It is a constant symbol
    return str(t.eval(V)) # Evaluate the expression
    
# Instantiate an atom for given variable bindings
# Atoms are pairs (pred,termlist)

def instantiateatom(a,bindings):
    pred,termlist = a
    itermlist = map( (lambda t : instantiateterm(t,bindings)) ,termlist)
    return (pred,itermlist)
#    return pred + "_" + '_'.join(itermlist)

# Instantiate a formula for given variable bindings

def instantiatefma(f,bindings):
    M = (lambda a : instantiateatom(a,bindings))
    return f.varmap(M)

# Go through all variable bindings

def doallassignments(params,formula,bindings):
    if params == []:
        return [instantiatefma(formula,bindings)]
    param,*params2 = params
    var,values = param
    result = [ doallassignments(params2,formula,bindings + [(var,val)]) for val in values ]
    return sum(result,[])

# Ground one formula

def groundformula(params,f):
    return doallassignments(params,f,list())

# Elimination of quantifiers forsome, forall, atleast, atmost, exactly

def Forsome(params,f): return DISJ(groundformula(params,f))
def Forall(params,f): return CONJ(groundformula(params,f))
def Atmost(N,params,f): return ATMOST(groundformula(params,f),N)
def Exactly(N,params,f): return EXACTLY(groundformula(params,f),N)
def Atleast(N,params,f):
    if N==1:
        return Forsome(params,f)
    else:
        return ATLEAST(groundformula(params,f),N)

# Top-level procedure for grounding.

def groundmodel(formulas):
#    for f in formulas:
#        print("FORMULA: ",end='')
#        print(str(f))
    def g(a):
        pred,termlist = a
        if len(termlist) == 0:
            return pred
        return pred + "_" + '_'.join(termlist)
    gformulas = [ f.atommap(g) for f in formulas ]
    allvars = sorted(set().union({ v for f in gformulas for v in f.vars()}))
#
#    for f in gformulas:
#        print("GFORMULA: ",end='')
#        print(str(f))
    return (gformulas,allvars)
