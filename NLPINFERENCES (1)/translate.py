#!/usr/bin/python3

from predlogic import *

# Exceptions

class EnglishSyntaxError(Exception):
    pass

class EnglishLexerError(Exception):
    pass

# We use the Ply package for generating a lexer and a parser

#################### Lexer

# All tokens used in the grammar. These denote the terminal
# symbols, that is, symbols recognized by the lexical analyzer
# which reads the textual input and recognizes the relevant
# syntactic object from it, which in this case is mostly words
# with a fixed meaning like "and" or "not", pre-defined words
# that form a specific category like transitive verbs
# consisting of "sees", "knows" and other words.
# The only non-word tokens are the period for the end of
# a sentence, and the single quote ' used in forming
# genitive like "John's". Our sentence separator =======
# consisting of one or more equal signs is also a token.

tokens = ('AND',
          'OR',
          'NOT',
          'SOME',
          'EVERY',
          'A',
          'THE',
          'NO',
          'IS',
          'OF',
          'THAT',
          'ID',
          'ivID',
          'tvID',
          'adjID',
          'roleID',
          'DOT',
          'SINGLEQUOTE',
          'S',
          'EQUALS'
)

# Definition of non-word tokens for the lexical analyzer

t_SINGLEQUOTE = r"'"
t_DOT = r'.'
t_EQUALS = r'=+'

# Characters to be ignored by the lexical analyzer
t_ignore = " \t"

# The following functions represent the lexical analyzer's rules
# for different tokens. There is first a regular expression to
# define the character sequences that are recgonized as the token.
# This is followed by Python code that either creates the token value
# (e.g. by assigning something to its 'type' field), or takes some
# action that leads to not returning a token at all, # like in
# the case of newlines, comments and lexical errors.

# When encountering the newline character, increase the line count.

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Comments are ignored by the lexical analyzer.
    
def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded.

# Process characters that are not handled by the lexer.
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    raise EnglishLexerError

# Mapping from reserved words to tokens

keywords = {'and' : 'AND',
            'or' : 'OR',
            'not' : 'NOT',
            'implies' : 'IMPLIES',
            'some' : 'SOME',
            'every' : 'EVERY',
            'a' : 'A',
            's' : 'S',
            'the' : 'THE',
            'no' : 'NO',
            'is' : 'IS',
            'of' : 'OF',
            'that' : 'THAT'
}

# Different categories of verbs, adjectives, as well as nouns that
# express binary relations. You can extend this if you want the
# program to cover a broader range of sentences.

transitiveVerbs = { 'sees', 'knows', 'likes', 'hears' }
intransitiveVerbs = { 'sleeps', 'walks', 'runs', 'snores' }
adjectives = { 'small', 'young', 'happy', 'sad' }
binaryrelations = { 'mother', 'father', 'parent', 'sibling', 'sister', 'brother', 'cousin', 'grandparent', 'grandmother', 'grandfather', 'uncle', 'aunt', 'niece', 'nephew', 'daughter' }

# Recognize an alphanumeric ID, and if it is one of the words
# with a fixed meaning, then map it to the corresponding token
# like tvID, ivID, adjID or roleID. The rest are treated as
# names (constant symbols) or common nouns (unary predicates).

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() in keywords:
        t.type = keywords[t.value.lower()]
    elif t.value.lower() in transitiveVerbs:
        t.type = 'tvID'
    elif t.value.lower() in intransitiveVerbs:
        t.type = 'ivID'
    elif t.value.lower() in adjectives:
        t.type = 'adjID'
    elif t.value.lower() in binaryrelations:
        t.type = 'roleID'
    return t
    
# Build the lexer with the Ply package

import ply.lex as lex
lexer = lex.lex()

####### Generation of new vars to be used in quantifications etc.

varcnt = 0
varnames0 = ["x","y","z","u","v","w"]
varnames = varnames0 + [ v + str(i) for v in varnames0 for i in range(100) ]

def newX():
    global varcnt
    varcnt = varcnt+1
    return varnames[varcnt-1]

####### The grammar rules for a fragment of English

##### Parsing rules
#
# The Ply parsing rules are expressed by the functions with a name
# starting ith "p_". The "comment" part expresses the LALR grammar
# rule, with a non-terminal symbol on the left-hand side, and the terminal
# and/or non-terminal symbols corresponding to the lhs non-terminal on
# the right-hand side. Multiple rules can be included in one function
# by combining several right-hand sides together with the vertical bar |,
# all being recognized as the non-terminal on the left-hand side.
#
# The code that follows the context-free grammar rule computes an attribute
# value to be associated with the non-terminal on the left-hand side,
# which is assigned to t[0]. The attribute values for the terminal and
# non-terminals on the right-hand side are stored in t[1], t[2], ..., t[N],
# when there are N symbols in the grammar rule(s).
#
# In our grammar, the attribute values associated with the various
# terminals and non-terminals are exactly the predicate logic formulas
# and lambda expressions that provide the semantics of each of the
# grammatical categories represented by the terminals and non-terminals.
# For example, in the grammar rule 'sentence : NP VP', we have
# certain lambda expressions as attributes of NP and VP, stored in
# t[1] and t[2], and then we compute the attribute value for the
# 'sentence' simply by calling the function t[1] with the input t[2],
# as discussed in the lecture. This attribute value is then stored in t[0].

##### Top-level definitions

def p_spec(t):
    '''spec : sentence0 spec'''
    t[0] = [t[1]] + t[2]

def p_spec1(t):
    '''spec : sentence0'''
    t[0] = [t[1]]

def p_sentence_separator(t):
    'sentence0 : EQUALS'
    t[0] = 0

def p_sentence_top(t):
    'sentence0 : sentence DOT'
    global varcnt
#    print("Parsed sentence: ",end='')
#    print(t[1])
    varcnt = 0
    t[0] = t[1]

def p_sentence(t):
    'sentence : NP VP'
    t[0] = (t[1])(t[2])

def p_sentence_or(t):
    'sentence : sentence OR sentence'
    t[0] = OR(t[1],t[3])

def p_NP_ID(t):
    'NP	: ID '
    IDstr = t[1] # Using t[1] below fails: ply does not bind t correctly!
    t[0] = (lambda P : P (Const(IDstr)))

def p_NP_DET_CN(t):
    'NP : DET CN'
    t[0] = (t[1])(t[2])

def p_NP_DET_RCN(t):
    'NP : DET RCN'
    t[0] = (t[1])(t[2])

def p_NP_DET_roleCNof(t):
    'NP : DET roleCNof'
    t[0] = (t[1])(t[2])

def p_DET_some(t):
    'DET : SOME'
    x = newX()
    t[0] = (lambda P : lambda Q : EXISTS(x,AND(P (Var(x)),Q (Var(x)))))

def p_DET_a(t):
    'DET : A'
    x = newX()
    t[0] = (lambda P : lambda Q : EXISTS(x,AND(P (Var(x)),Q (Var(x)))))

def p_DET_the(t): # Exactly the same as A
    'DET : THE'
    x = newX()
    t[0] = (lambda P : lambda Q : EXISTS(x,AND(P (Var(x)),Q (Var(x)))))

def p_DET_every(t):
    'DET : EVERY'
    x = newX()
    t[0] = (lambda P : lambda Q : FORALL(x,IMPL(P (Var(x)),Q (Var(x)))))

def p_DET_no(t):
    'DET : NO'
    x = newX()
    t[0] = (lambda P : lambda Q : FORALL(x,IMPL(P (Var(x)),NOT(Q (Var(x))))))

def p_roleCNofWITHs(t):
    'NP : ID SINGLEQUOTE S roleID'
    IDstr = t[1]
    roleIDstr = t[4]
    x = newX()
    t[0] = lambda Q : EXISTS(x,AND(ATOM(roleIDstr,[Var(x),Const(IDstr)]),Q (Var(x))))

def p_VP_and(t):
    'VP : VP AND VP'
    VPf1 = t[1]
    VPf3 = t[3]
    t[0] = lambda t : AND(VPf1(t),VPf3(t))

def p_VP_ivID(t):
    'VP : ivID'
    ivIDstr = t[1]
    t[0] = (lambda x : ATOM(ivIDstr,[x]))

def p_VP_issame(t):
    'VP : IS NP'
    NPf = t[2]
    t[0] = (lambda x : NPf (lambda y : EQUAL(x,y)))

def p_VP_isnotsame(t):
    'VP : IS NOT NP'
    NPf = t[3]
    t[0] = (lambda x : NOT(NPf (lambda y : EQUAL(x,y))))

def p_VP_isADJ(t):
    'VP : IS adjID'
    adjIDstr = t[2]
    t[0] = lambda x : ATOM(adjIDstr,[x])

def p_VP_isADJnot(t):
    'VP : IS NOT adjID'
    adjIDstr = t[3]
    t[0] = lambda x : NOT(ATOM(adjIDstr,[x]))

def p_VP_TV_NP(t):
    'VP : TV NP'
    TVf = t[1]
    NPf = t[2]
    t[0] = (lambda x : NPf (lambda y : (TVf(y))(x)))

def p_TV_tvID(t):
    'TV : tvID'
    tvIDstr = t[1]
    t[0] = (lambda y : lambda x : ATOM(tvIDstr,[x,y]))

def p_RCN_CN_that_VP(t):
    'RCN : CN THAT VP'
    CNf = t[1]
    VPf = t[3]
    t[0] = (lambda x : AND(CNf(x),VPf(x)))

def p_RCN_CN_that_NP_TV(t):
    'RCN : CN THAT NP TV'
    CNf = t[1]
    NPf = t[3]
    TVf = t[4]
    t[0] = (lambda x : AND(CNf(x),NPf (lambda y : (TVf(y))(x))))

def p_roleCNof(t):
    'roleCNof : roleID OF NP'
    roleIDstr = t[1]
    NPf = t[3]
    t[0] = (lambda x : NPf (lambda y : ATOM(roleIDstr,[x,y])))

def p_CN_ID(t):
    'CN : ID'
    IDstr = t[1]
    t[0] = (lambda x : ATOM(IDstr,[x]))

def p_CN_ADJ_CN(t):
    'CN : adjID CN'
    adjIDstr = t[1]
    CNf = t[2]
    t[0] = (lambda x : AND(ATOM(adjIDstr,[x]),CNf(x)))

# Error rule

def p_error(t):
    print("Syntax error at '%s'" % t.value)
    print("On line " + str(t.lexer.lineno))
    raise EnglishSyntaxError

# Build the parser with the Ply package

import ply.yacc as yacc
parser = yacc.yacc()

# Parse one string and return the result

def parsestring(s):
    return parser.parse(s)

# Read the whole input file, and parse it

def parseinputfile(filename):
    with open(filename, 'r') as f:
        allinput = f.read()
        sentences = parser.parse(allinput)
    if len(sentences) < 1:
        print("Must give at least one sentence.")
        exit(1)
    print("Parsed " + str(len(sentences)) + " sentences:")
    for i in range(len(sentences)):
        if sentences[i] == 0:
            return sentences[:i],[ s for s in sentences[i:] if s != 0 ]
    return sentences,[]

###### Definitions of concepts that express family relations
#
# These will be part of the output in the TPTP format, so that
# English sentences that assume certain fixed meanings for
# words that refer to family relationships can be interpreted
# better.

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
daughter = lambda x,y : ATOM("daughter",[x,y])
aunt = lambda x,y : ATOM("aunt",[x,y])
uncle = lambda x,y : ATOM("uncle",[x,y])
nephew = lambda x,y : ATOM("nephew",[x,y])
grandparent = lambda x,y : ATOM("grandparent",[x,y])
grandmother = lambda x,y : ATOM("grandmother",[x,y])
sibling = lambda x,y : ATOM("sibling",[x,y])
cousin = lambda x,y : ATOM("cousin",[x,y])

# Long ANDs expressed as a list

def chainAND(l):
  if l == []:
    return TRUE()
  elif len(l) == 1:
    return l[0]
  else:
    return AND(l[0],chainAND(l[1:]))

# Definitions of family relationships:
# Mother, father, sister, brother, aunt, uncle, nephew, sibling, cousin,
# daugher in terms of parent, female, male

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
A12 = FORALL("x",FORALL("y",EQVI(daughter(x,y),AND(female(x),parent(y,x)))))

# Female and male are mutually exclusive.

A13 = FORALL("x",NOT(AND(female(x),male(x))))

# Sibling relation is symmetric.

A14 = FORALL("x",FORALL("y",EQVI(sibling(x,y),
                                 sibling(y,x))))

# Assumption: siblings have exactly the same parents (so no half-siblings).

A15 = FORALL("x",FORALL("y",FORALL("z",IMPL(sibling(x,y),
                                            EQVI(parent(z,x),
                                                 parent(z,y))))))

# Only one mother and one father.

A16 = FORALL("x",FORALL("y",FORALL("z",IMPL(AND(mother(x,y),mother(z,y)),
                                            EQUAL(x,z)))))
A17 = FORALL("x",FORALL("y",FORALL("z",IMPL(AND(father(x,y),father(z,y)),
                                            EQUAL(x,z)))))

familyrelations = [A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17]

# Show formulas and generate TPTP output

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        inputfilename = 'TEXT'
    else:
        inputfilename = sys.argv[1]
    if len(sys.argv) < 3:
        outputfilename = 'OUTPUT.TPTP'
    else:
        outputfilename = sys.argv[2]
    try:
        premises,conclusions = parseinputfile(inputfilename)
    except EnglishSyntaxError:
        print("Syntax error, exiting...\n")
        exit(1)
    except EnglishLexerError:
        print("Lexer error, exiting...\n")
        exit(1)
    for f in premises:
        print(str(f))
    print("===========================================")
    for f in conclusions:
        print(str(f))
    print("")
    tptpfile = open(outputfilename,"w")
    i = 0
    # Output everything, including the family relations to the TPTP file
    for f in familyrelations + premises:
        i = i+1
        tptpfile.write("fof(formula" + str(i) + ",axiom, (" + f.TPTP() + ")).\n")
    for f in conclusions:
        i = i+1
        tptpfile.write("fof(formula" + str(i) + ",conjecture, (" + f.TPTP() + ")).\n")
    tptpfile.close()
