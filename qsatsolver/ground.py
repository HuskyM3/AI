
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

def getBinding(x,bindings):
    for e in bindings:
        k,v = e
        if k==x: return v # It is a bound variable
    return VAR(x)
    print("No binding for variable '" + x + "'")
    
# Instantiate an atom for given variable bindings
# Atoms are pairs (pred,termlist)

def substAtom(a,bindings):
    pred,termlist = a
    f = (lambda v : getBinding(v,bindings))
    itermlist = [ t.varmap(f) for t in termlist ]
    return (pred,itermlist)

# Instantiate a formula for given variable bindings

def instantiatefma(f,bindings):
    M = (lambda a : substAtom(a,bindings))
    return f.atommap(M)

# Go through all variable bindings

def doallassignments(params,formula,bindings):
    if params == []:
        return [instantiatefma(formula,bindings)]
    param,*params2 = params
    var,values = param
    result = [ doallassignments(params2,formula,bindings + [(var,val)]) for val in values ]
    return sum(result,[])

# Substitute a variable with a value

def substFma(params,f):
    return doallassignments(params,f,list())

# Elimination of quantifiers forsome, forall, atleast, atmost, exactly

def Forsome(params,f): return DISJ(substFma(params,f))
def Forall(params,f):
    ff = CONJ(substFma(params,f))
    return ff
def Atmost(N,params,f): return ATMOST(substFma(params,f),N)
def Exactly(N,params,f): return EXACTLY(substFma(params,f),N)
def Atleast(N,params,f):
    if N==1:
        return Forsome(params,f)
    else:
        return ATLEAST(substFma(params,f),N)

# Evaluate all arithmetics and turn everything to atoms.

def propositionalize(formulas):
#    for f in formulas:
#        print("FORMULA: ",end='')
#        print(str(f))
    V = (lambda x : STRCONST(x))
    def g(a):
        pred,termlist = a
        if len(termlist) == 0:
            return pred
        return pred + "_" + '_'.join([ str(t.eval(V)) for t in termlist])
    gformulas = [ f.atommap(g) for f in formulas ]
    allvars = sorted(set().union({ v for f in gformulas for v in f.vars()}))
#
#    for f in gformulas:
#        print("GFORMULA: ",end='')
#        print(str(f))
    return (gformulas,allvars)

# Solution
#
# 
