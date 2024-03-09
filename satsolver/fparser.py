
class LogicSyntaxError(Exception):
    pass

class LogicLexerError(Exception):
    pass

from formulas import *
from ground import *

#################### Lexer

# all tokens

tokens = (
    'ID', 'NID', 'NUMBER',
    'AND','OR','NOT','XOR','EQVI','IMPL',
    'LPAREN','RPAREN',
    'LEQ', 'GEQ', 'LT', 'GT', 'EQ',
    'PLUS', 'MINUS', 'TIMES',
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

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Is the ID actually a keyword?

    if t.value in keywords:
        t.type = keywords[t.value]

    # Has the ID been declared as a variable/predicate?

#    if t.value in predicates:
#        t.type = 'PID'

    # Something else
    return t
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

####### Data to be filled in by the parser/lexer

# dictionary of types
names = { }

# set of formulas
formulas = list()

# dictionary of predicates/variables

predicates = dict()

####### Parser

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES'),
    ('right','EQVI'),
    ('right','IMPL'),
    ('left','AND','OR','XOR'),
    ('left','NOT')
    )

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
    'predlist : ID SLASH NUMBER'
    t[0] = [(t[1],t[3])]

def p_predlistN(t):
    'predlist : ID SLASH NUMBER COMMA predlist'
    t[0] = [(t[1],t[3])] + t[5]

# variable declaration

def p_variables_definition(t):
    'statement : VARIABLES idlist SEMICOLON'
    for v in t[2]: predicates[v] = 0

def p_idlist1(t):
    'idlist : ID'
    t[0] = [t[1]]

def p_idlistN(t):
    'idlist : ID COMMA idlist'
    t[0] = [t[1]] + t[3]


# type definition

def p_type_definition(t):
    'statement : TYPE ID EQ setexpr SEMICOLON'
    names[t[2]] = t[4]

# formula

def p_formula(t):
    'statement : boolexpr SEMICOLON'
    formulas.append(t[1])

def p_setexpr_interval(t):
    'setexpr : LBRACK NUMBER COMMA NUMBER RBRACK'
    t[0] = { x for x in range(t[2],t[4]+1) }

def p_setexpr_enumed(t):
    'setexpr : LBRACE stringlist RBRACE'
    t[0] = t[2]

def p_setexpr_named(t):
    'setexpr : ID'
    t[0] = names[t[1]]

def p_stringlist1(t):
    'stringlist : enum'
    t[0] = { t[1] }

def p_enum(t):
    '''enum : ID
            | NUMBER'''
    t[0] = t[1]

def p_stringlistN(t):
    'stringlist : enum COMMA stringlist'
    t[0] = t[3].union({ t[1] })

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

# Existential and universal quantification

def p_boolexpr_quant_ex(t):
    '''boolexpr : FORSOME LPAREN paramlist RPAREN boolexpr'''
    t[0] = Forsome(t[3],t[5])

def p_boolexpr_quant_un(t):
    '''boolexpr : FORALL LPAREN paramlist RPAREN boolexpr'''
    t[0] = Forall(t[3],t[5])

# Cardinality quantification    

def p_boolexpr_quant_atmost(t):
    '''boolexpr : ATMOST NUMBER LPAREN paramlist RPAREN boolexpr'''
    t[0] = Atmost(t[2],t[4],t[6])

def p_boolexpr_quant_atleast(t):
    '''boolexpr : ATLEAST NUMBER LPAREN paramlist RPAREN boolexpr'''
    t[0] = Atleast(t[2],t[4],t[6])

def p_boolexpr_quant_exactly(t):
    '''boolexpr : EXACTLY NUMBER LPAREN paramlist RPAREN boolexpr'''
    t[0] = Exactly(t[2],t[4],t[6])

# Negation
    
def p_boolexpr_unop(t):
    'boolexpr : NOT boolexpr'
    t[0] = NEG(t[2])

def p_boolexpr_atom(t):
    'boolexpr : atom'
    t[0] = AT(t[1])

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
    t[0] = (t[1],t[3])
    
# Numeric expressions

def p_numexpr_parentheses(t):
    '''numexpr : LPAREN numexpr RPAREN'''
    t[0] = t[2]

def p_numexpr1(t):
    'numexpr : NUMBER'
    t[0] = NumINTCONST(t[1])

def p_numexpr2(t):
    'numexpr : NID'
    t[0] = NumINTVAR(t[1])

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

# Atoms (Boolean valued state variables P(t1,...,tn) consisting of
#        a predicate symbol P and a list of terms t1,...,tn)

def p_atom0(t):
    'atom : ID'
    t[0] = (t[1],list())

def p_atom(t):
    'atom : ID LPAREN termlist RPAREN'
    t[0] = (t[1],t[3])

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
    return groundmodel(formulas)
