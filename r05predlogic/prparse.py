#!/usr/bin/python3

from predlogic import *

# Exceptions

class FormulaSyntaxError(Exception):
    pass

class FormulaLexerError(Exception):
    pass

# Predicate and constant symbols

parser_constants = []
parser_predicates = dict()

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
          'FORALL',
          'EXISTS',
          'EQ',
          'NEQ',
          'IMPLIES',
          'EQVI',
          'LPAREN',
          'RPAREN',
          'COMMA',
          'ID'
)

# Definition of non-word tokens for the lexical analyzer

t_EQ = r'='
t_NEQ = r'!='
t_AND = r'\&'
t_OR = r'\|'
t_NOT = r'\~'
t_IMPLIES = r'=>'
t_EQVI = r'<=>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r'\,'

# Characters to be ignored by the lexical analyzer
t_ignore = " \t"

# The following functions represent the lexical analyzer's rules
# for different tokens. There is first a regular expression to
# define the character sequences that are recgonized as the token.
# This is followed by Python code that either creates the token value
# (e.g. by assigning something to its 'type' field), or takes some
# action that leads to not returning a token at all, # like in
# the case of newlines, comments and lexical errors.

precedence = (
    ('right','EQVI'),
    ('right','IMPLIES'),
    ('left','AND','OR'),
    ('left','NOT'),
    ('left','FORALL','EXISTS'),
    )

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
    raise FormulaLexerError

# Mapping from reserved words to tokens

keywords = {'and' : 'AND',
            'or' : 'OR',
            'not' : 'NOT',
            'implies' : 'IMPLIES',
            'forall' : 'FORALL',
            'exists' : 'EXISTS'
}

# Recognize an alphanumeric ID, and if it is one of the words
# with a fixed meaning, then map it to the corresponding token
# like tvID, ivID, adjID or roleID. The rest are treated as
# names (constant symbols) or common nouns (unary predicates).

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() in keywords:
        t.type = keywords[t.value.lower()]
    return t
    
# Build the lexer with the Ply package

import ply.lex as lex
formulalexer = lex.lex()

sentences = []

####### Generation of new vars to be used in quantifications etc.

varcnt = 0
varnames0 = ["x","y","z","u","v","w"]
varnames = varnames0 + [ v + str(i) for v in varnames0 for i in range(100) ]

##### Parsing rules
#

##### Top-level definitions

def p_spec_0(t):
    '''spec : '''
    t[0] = []

def p_spec(t):
    '''spec : boolexpr spec'''
    t[0] = [ t[1] ] + t[2]

# Boolean expressions

def p_forall_quant(t):
    '''boolexpr : FORALL ID uboolexpr'''
    t[0] = FORALL(t[2],t[3])

def p_u_forall_quant(t):
    '''uboolexpr : FORALL ID uboolexpr'''
    t[0] = FORALL(t[2],t[3])

def p_uboolexpr_parent(t):
    'uboolexpr : LPAREN boolexpr RPAREN'
    t[0] = t[2]

def p_uboolexpr_atom(t):
    'uboolexpr : atom'
    global parser_predicates
    pred,terms = t[1]
    if pred not in parser_predicates:
        print("Undefined predicate '" + pred + "' in the formula file (line " + str(t.lexer.lineno) + ")")
        raise FormulaSyntaxError
    if len(terms) != parser_predicates[pred]:
        print("Predicate '" + pred + "' arity is " + str(parser_predicates[pred]) + " but " + str(len(terms)) + " terms in atom '" + str(ATOM(pred,terms)) + "' (line " + str(t.lexer.lineno) + ")")
        raise FormulaSyntaxError
    t[0] = ATOM(pred,terms)

def p_exists_quant(t):
    '''boolexpr : EXISTS ID uboolexpr'''
    t[0] = EXISTS(t[2],t[3])

def p_u_exists_quant(t):
    '''uboolexpr : EXISTS ID uboolexpr'''
    t[0] = EXISTS(t[2],t[3])

def p_boolexpr_binop(t):
    '''boolexpr : boolexpr AND boolexpr
                | boolexpr OR boolexpr
                | boolexpr IMPLIES boolexpr
                | boolexpr EQVI boolexpr'''
    if t[2] == 'and'   : t[0] = AND(t[1],t[3])
    elif t[2] == 'or'  : t[0] = OR(t[1],t[3])
    elif t[2] == 'impl': t[0] = IMPL(t[1],t[3])
    elif t[2] == 'eqvi': t[0] = EQVI(t[1],t[3])
    elif t[2] == '&'   : t[0] = AND(t[1],t[3])
    elif t[2] == '|'  : t[0] = OR(t[1],t[3])
    elif t[2] == '=>': t[0] = IMPL(t[1],t[3])
    elif t[2] == '<=>': t[0] = EQVI(t[1],t[3])
    else:
        print("Internal error")
        exit(1)

def p_boolexpr_unop(t):
    'boolexpr : NOT boolexpr'
    t[0] = NOT(t[2])

def p_boolexpr_eq(t):
    'boolexpr : term EQ term'
    t[0] = EQUAL(t[1],t[3])

def p_boolexpr_neq(t):
    'boolexpr : term NEQ term'
    t[0] = NOT(EQUAL(t[1],t[3]))

def p_boolexpr_atom(t):
    'boolexpr : atom'
    global parser_predicates
    pred,terms = t[1]
    if pred not in parser_predicates:
        print("Undefined predicate '" + pred + "' in the formula file (line " + str(t.lexer.lineno) + ")")
        raise FormulaSyntaxError
    if len(terms) != parser_predicates[pred]:
        print("Predicate '" + pred + "' arity is " + str(parser_predicates[pred]) + " but " + str(len(terms)) + " terms in atom '" + str(ATOM(pred,terms)) + "' (line " + str(t.lexer.lineno) + ")")
        raise FormulaSyntaxError
    t[0] = ATOM(pred,terms)

def p_boolexpr_parentheses(t):
    '''boolexpr : LPAREN boolexpr RPAREN'''
    t[0] = t[2]

# Terms (part of an atom)

def p_termlistN(t):
    'termlist : term COMMA termlist'
    t[0] = [t[1]] + t[3]

def p_termlist1(t):
    'termlist : term'
    t[0] = [t[1]]

def p_term(t):
    'term : ID'
    global parser_constants
    if t[1] in parser_constants:
        t[0] = Const(t[1])
    else:
        t[0] = Var(t[1])

# Atoms (Boolean valued state variables P(t1,...,tn) consisting of
#        a predicate symbol P and a list of terms t1,...,tn)

def p_atom(t):
    'atom : ID LPAREN termlist RPAREN'
    t[0] = (t[1],t[3])

# Error rule

def p_error(t):
    print("Syntax error at '%s'" % t.value)
    print("On line " + str(t.lexer.lineno) + " in formulas")
    raise FormulaSyntaxError

# Build the parser with the Ply package

import ply.yacc as yacc
parser = yacc.yacc()

# Read the whole input file, and parse it

def parseFormulaFile(filename,predicates,constants):
    global parser_constants
    global parser_predicates
    
    parser_predicates = predicates
    parser_constants = constants

    print("Parsing '" + filename + "'")

    with open(filename, 'r') as f:
        allformulas = parser.parse(f.read(),lexer=formulalexer)
    if len(allformulas) < 1:
        print("Must give at least one formula.")
        raise FormulaSyntaxError
    for f in allformulas:
        if len(f.freeVars()) > 0:
            print("Formula '" + str(f) + "' has free variables: " + " ,".join(f.freeVars()))
            print("Cannot evaluate truth-value!")
            raise FormulaSyntaxError
    return allformulas
