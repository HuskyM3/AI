
class LogicSyntaxError(Exception):
    pass

class LogicLexerError(Exception):
    pass

from formulas import *
from ground import *

#################### Lexer

# all tokens

tokens = (
    'ID', 'PID', 'NUMBER',
    'AND','OR','NOT','XOR','EQVI','IMPL',
    'LPAREN','RPAREN',
    'LEQ', 'GEQ', 'LT', 'GT', 'EQ',
    'PLUS', 'MINUS', 'TIMES',
    'UNION',
    'SLASH',
    'FORALL', 'FORSOME',
    'EXACTLY', 'ATMOST', 'ATLEAST',
    'VARIABLES', 'PREDICATES',
    'COLON', 'SEMICOLON', 'COMMA',
    'LBRACK', 'RBRACK',
    'LBRACE', 'RBRACE',
    'TYPE'
    )

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_EQ      = r'='
t_SLASH   = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACK  = r'\['
t_RBRACK  = r'\]'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r'\,'
t_LEQ = r'\<\='
t_GEQ = r'\>\='
t_LT = r'\<'
t_GT = r'\>'
t_EQVI = r'\<-\>'
t_IMPL = r'-\>'
t_AND = r'&'
t_OR = r'\|'

# Numbers

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

# Process characters that are not handled by the lexer
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    raise LogicLexerError

# IDs and reserved words

# Mapping from reserved words to tokens

keywords = {'and': 'AND',
            'or': 'OR',
            'not': 'NOT',
            'xor': 'XOR',
            'eqvi': 'EQVI',
            'impl': 'IMPL',
            'type': 'TYPE',
            'forsome': 'FORSOME',
            'forall': 'FORALL',
            'exists': 'FORSOME',
            'exactly': 'EXACTLY',
            'atmost': 'ATMOST',
            'atleast': 'ATLEAST',
            'variables' : 'VARIABLES',
            'predicates' : 'PREDICATES'
            }

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES'),
    ('left','UNION'),
    ('right','EQVI'),
    ('right','IMPL'),
    ('left','AND','OR','XOR'),
    ('right','NOT'),
    ('right','FORSOME','FORALL','EXACTLY','ATLEAST','ATMOST'),
    ('nonassoc','GT','LT','EQ','LEQ','GEQ'),
    )

# IDs for term variables start with a lower case letter

def t_ID(t):
    r'[a-z][a-zA-Z0-9_]*'

    # Is the ID actually a keyword?

    if t.value in keywords:
        t.type = keywords[t.value]

    return t
    
# IDs for predicate/propositional variables start with an upper case letter

def t_PID(t):
    r'[A-Z][a-zA-Z0-9_]*'

    # Is the PID actually a keyword?

    if t.value in keywords:
        t.type = keywords[t.value]

    if t.value == "U":
        t.type = 'UNION'

    return t
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

####### Data to be filled in by the parser/lexer

# dictionary of types

typenames = dict()

# set of formulas

formulas = list()

# dictionary of predicates/variables

predicates = dict()

# constant symbols

constantsymbols = set()

####### Parser

# Parsing rules

# Top-level definitions

def p_spec(t):
    '''spec : statement
            | statement spec'''
    t[0] = 0

# predicate declaration

def p_predicates_definition(t):
    'statement : PREDICATES predlist SEMICOLON'
    for p,a in t[2]:
        predicates[p] = a

def p_predlist1(t):
    'predlist : PID SLASH NUMBER'
    t[0] = [(t[1],t[3])]

def p_predlistN(t):
    'predlist : PID SLASH NUMBER COMMA predlist'
    t[0] = [(t[1],t[3])] + t[5]

# variable declaration

def p_variables_definition(t):
    'statement : VARIABLES idlist SEMICOLON'
    for v in t[2]: predicates[v] = 0

def p_idlist1(t):
    'idlist : PID'
    t[0] = [t[1]]

def p_idlistN(t):
    'idlist : PID COMMA idlist'
    t[0] = [t[1]] + t[3]

# Upper and lower case characters

def p_id(t):
    '''id : ID
          | PID'''
    t[0] = t[1]

# type definition

def p_type_definition(t):
    '''statement : TYPE id EQ setexpr SEMICOLON'''
    typenames[t[2]] = t[4]

# formula

def p_formula(t):
    '''statement : boolexpr SEMICOLON'''
    formulas.append(t[1])

def p_setexpr_interval(t):
    '''setexpr : LBRACK NUMBER COMMA NUMBER RBRACK'''
    t[0] = { NumINTCONST(x) for x in range(t[2],t[4]+1) }

def p_setexpr_enumed(t):
    '''setexpr : LBRACE valuelist RBRACE'''
    t[0] = t[2]

def p_setexpr_named(t):
    '''setexpr : id'''
    t[0] = typenames[t[1]]

def p_setexpr_union(t):
    '''setexpr : setexpr UNION setexpr'''
    t[0] = t[1].union(t[3])

def p_setexpr_difference(t):
    '''setexpr : setexpr MINUS setexpr'''
    t[0] = t[1].difference(t[3])

def p_valuelist1(t):
    '''valuelist : value'''
    t[0] = { t[1] }

def p_valuelistN(t):
    '''valuelist : value COMMA valuelist'''
    t[0] = t[3].union({ t[1] })

def p_value_id(t):
    '''value : ID'''
    t[0] = STRCONST(t[1])

def p_value_num(t):
    '''value : NUMBER'''
    t[0] = NumINTCONST(t[1])

# Boolean expressions

def p_boolexpr_and(t):
    '''boolexpr : boolexpr AND boolexpr'''
    t[0] = CONJ([t[1],t[3]])

def p_boolexpr_or(t):
    '''boolexpr : boolexpr OR boolexpr'''
    t[0] = DISJ([t[1],t[3]])

def p_boolexpr_xor(t):
    '''boolexpr : boolexpr XOR boolexpr'''
    t[0] = XDISJ(t[1],t[3])

def p_boolexpr_impl(t):
    '''boolexpr : boolexpr IMPL boolexpr'''
    t[0] = IMPL(t[1],t[3])

def p_boolexpr_eqvi(t):
    '''boolexpr : boolexpr EQVI boolexpr'''
    t[0] = EQVI(t[1],t[3])

# Rule for unary operators

def p_boolexpr_unop(t):
    'boolexpr : unop uboolexpr'
    f = t[1]
    t[0] = f(t[2])

def p_uboolexpr_parent(t):
    'uboolexpr : LPAREN boolexpr RPAREN'
    t[0] = t[2]

def p_uboolexpr_unop(t):
    'uboolexpr : unop uboolexpr'
    f = t[1]
    t[0] = f(t[2])

def p_uboolexpr_atom(t):
    'uboolexpr : atom'
    t[0] = AT(t[1])

# Existential and universal quantification
 
def p_unop_quant_ex(t):
    '''unop : FORSOME LPAREN paramlist RPAREN'''
    t[0] = (lambda b,i=t[3]: Forsome(i,b))

def p_unop_quant_univ(t):
    '''unop : FORALL LPAREN paramlist RPAREN'''
    t[0] = (lambda b,i=t[3]: Forall(i,b))

# Cardinality quantification    

def p_unop_quant_atmost(t):
    '''unop : ATMOST NUMBER LPAREN paramlist RPAREN'''
    t[0] = (lambda b,i=t[2],j=t[4]: Atmost(i,j,b))

def p_unop_quant_atleast(t):
    '''unop : ATLEAST NUMBER LPAREN paramlist RPAREN'''
    t[0] = (lambda b,i=t[2],j=t[4]: Atleast(i,j,b))

def p_unop_quant_exactly(t):
    '''unop : EXACTLY NUMBER LPAREN paramlist RPAREN'''
    t[0] = (lambda b,i=t[2],j=t[4]: Exactly(i,j,b))

# Negation
    
#def p_boolexpr_NOT(t):
#    'boolexpr : NOT boolexpr'
#    t[0] = NEG(t[2])

def p_unop_NOT(t):
    '''unop : NOT'''
    t[0] = (lambda b: NEG(b))

# Atoms are formulas

def p_boolexpr_atom(t):
    'boolexpr : atom'
    t[0] = AT(t[1])

# Atoms (Boolean valued state variables P(t1,...,tn) consisting of
#        a predicate symbol P and a list of terms t1,...,tn)

def p_atom0(t):
    'atom : PID'
    if t[1] not in predicates:
        print("No predicate '" + t[1] + "' has been declared")
        print("On line " + str(t.lexer.lineno))
        raise LogicSyntaxError
    if predicates[t[1]] > 0:
        print("Predicate " + t[1] + " has arity " + str(predicates[t[1]]))
        print("On line " + str(t.lexer.lineno))
        raise LogicSyntaxError
    t[0] = (t[1],list())

def p_atom(t):
    'atom : PID LPAREN termlist RPAREN'
    if t[1] not in predicates:
        print("No predicate '" + t[1] + "' has been declared")
        print("On line " + str(t.lexer.lineno))
        raise LogicSyntaxError
    if len(t[3]) != predicates[t[1]]:
        print("Predicate " + t[1] + " has arity " + str(predicates[t[1]]) + ": " + str(t[3]))
        print("On line " + str(t.lexer.lineno))
        raise LogicSyntaxError
    t[0] = (t[1],t[3])

# Parentheses

def p_boolexpr_parentheses(t):
    '''boolexpr : LPAREN boolexpr RPAREN'''
    t[0] = t[2]

def p_boolexpr_numrel(t):
    '''boolexpr : numexpr GT numexpr
                | numexpr LT numexpr
                | numexpr GEQ numexpr
                | numexpr LEQ numexpr
                | numexpr EQ numexpr'''
    t[0] = NUMREL(t[1],t[2],t[3])

# quantifier parameters

def p_paramlist1(t):
    '''paramlist : param'''
    t[0] = [ t[1] ]

def p_paramlistN(t):
    '''paramlist : param COMMA paramlist'''
    t[0] = [ t[1] ] + t[3]

def p_param(t):
    '''param : ID COLON setexpr'''
    if t[1] in constantsymbols:
        print("Ambiguity: " + t[1] + " occurs as both variable and a constant symbol")
        print("On line " + str(t.lexer.lineno))
        raise LogicSyntaxError
    constantsymbols.update({ t.value for t in t[3] if isinstance(t,STRCONST)})
    t[0] = (t[1],t[3])
    
# Numeric expressions

def p_numexpr_parentheses(t):
    '''numexpr : LPAREN numexpr RPAREN'''
    t[0] = t[2]

def p_numexpr1(t):
    'numexpr : NUMBER'
    t[0] = NumINTCONST(t[1])

def p_numexpr2(t):
    'numexpr : ID'
    if t[1] in constantsymbols:
        t[0] = STRCONST(t[1])
    else:
        t[0] = VAR(t[1])

def p_numexpr(t):
    '''numexpr : numexpr PLUS numexpr
               | numexpr MINUS numexpr
               | numexpr TIMES numexpr'''
    if t[2] == '+': t[0] = NumPLUS(t[1],t[3])
    elif t[2] == '-' : t[0] = NumMINUS(t[1],t[3])
    elif t[2] == '*' : t[0] = NumTIMES(t[1],t[3])

# Terms (part of an atom)

def p_termlistN(t):
    'termlist : term COMMA termlist'
    t[0] = [t[1]] + t[3]

def p_termlist1(t):
    'termlist : term'
    t[0] = [t[1]]

# Terms can be numbers, computed from an arithmetic expressions

def p_term_numeric(t):
    'term : numexpr'
    t[0] = t[1]

# Error rule

def p_error(t):
    print("Syntax error at '%s'" % t.value)
    print("On line " + str(t.lexer.lineno))
    raise LogicSyntaxError

import ply.yacc as yacc
parser = yacc.yacc()

def parseinputfile(filename):
    with open(filename, 'r') as f:
        allinput = f.read()
        parser.parse(allinput)
    for s in constantsymbols:
        print("CONSTANT: " + s)
    return propositionalize(formulas)
