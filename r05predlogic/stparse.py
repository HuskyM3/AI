#!/usr/bin/python3

from predlogic import *

class StructureSyntaxError(Exception):
    pass

class StructureLexerError(Exception):
    pass

# We use the Ply package for generating a lexer and a parser

#################### Lexer

# All tokens used in the grammar. These denote the terminal
# symbols, that is, symbols recognized by the lexical analyzer
# which reads the textual input and recognizes the relevant
# syntactic object from it, which in this case is mostly words
# with a fixed meaning like "and" or "not".


tokens = ('ID',
          'INT',
          'MINUS',
          'PLUS',
          'INTERSECT',
          'COMMA',
          'LBRACE',
          'RBRACE',
          'LPAREN',
          'RPAREN',
          'EQ',
          'SLASH'
)

# Definition of non-word tokens for the lexical analyzer

t_EQ = r'='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SLASH = r'\/'
t_INTERSECT = r'/\\'
t_COMMA = r'\,'

# The following functions represent the lexical analyzer's rules
# for different tokens. There is first a regular expression to
# define the character sequences that are recgonized as the token.
# This is followed by Python code that either creates the token value
# (e.g. by assigning something to its 'type' field), or takes some
# action that leads to not returning a token at all, # like in
# the case of newlines, comments and lexical errors.

precedence = (
    ('left','INTERSECT'),
    ('left','MINUS','PLUS'),
    )

# Ignored characters
t_ignore = " \t"

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
    raise StructureLexerError


# Numbers

def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Recognize an alphanumeric ID, and if it is one of the words
# with a fixed meaning, then map it to the corresponding token
# like tvID, ivID, adjID or roleID. The rest are treated as
# names (constant symbols) or common nouns (unary predicates).

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t
    
# Build the lexer with the Ply package

import ply.lex as lex
structlexer = lex.lex()

# All data collected from a specification file

predicates = dict()
predicate_arities = dict()
constants = dict()
universe = []

##### Parsing rules
#

# Top-level definitions

def p_spec(t):
    '''spec : LBRACE objlist RBRACE decls'''
    global universe
    universe = t[2]
    t[0] = 0

def p_decls(t):
    '''decls : 
             | decl decls'''
    t[0] = 0

# Boolean expressions

def p_decl_predicate(t):
    '''decl : ID SLASH INT EQ setexpr'''
    global predicates, predicate_arities
    predicate_arities[t[1]] = t[3]
    if any(len(e) != t[3] for e in t[5]):
        print("Arity " + str(t[3]) + " of predicate '" + t[1] + "' mismatched with some of the relation elements.")
        raise StructureSyntaxError
    predicates[t[1]] = t[5]
    t[0] = 0

def p_decl_constant_id(t):
    '''decl : ID EQ ID'''
    global constants
    constants[t[1]] = t[3]

def p_decl_constant_int(t):
    '''decl : ID EQ INT'''
    global constants
    constants[t[1]] = str(t[3])

def p_setexpr_enum0(t):
    '''setexpr : LBRACE RBRACE'''
    t[0] = []

def p_setexpr_enum(t):
    '''setexpr : LBRACE elements RBRACE'''
    t[0] = t[2]

def p_elements(t):
    '''elements : element COMMA elements'''
    t[0] = [ t[1] ] + t[3]
        
def p_elements1(t):
    '''elements : element'''
    t[0] = [ t[1] ]

def p_element_id(t):
    '''element : ID'''
    t[0] = [ t[1] ]

def p_element_int(t):
    '''element : INT'''
    t[0] = [ str(t[1]) ]

def p_element_tuple(t):
    '''element : LPAREN objlist RPAREN'''
    t[0] = t[2]

def p_objlist(t):
    '''objlist : obj COMMA objlist'''
    t[0] = [ t[1] ] + t[3]

def p_objlist_1(t):
    '''objlist : obj'''
    t[0] = [ t[1] ]

def p_obj_int(t):
    '''obj : INT'''
    t[0] = str(t[1])

def p_obj_id(t):
    '''obj : ID'''
    t[0] = t[1]

# Set operations

def p_setexpr_union(t):
    '''setexpr : setexpr PLUS setexpr'''
    t[0] = t[1].union(t[3])

def p_setexpr_intersection(t):
    '''setexpr : setexpr INTERSECT setexpr'''
    t[0] = t[1].intersection(t[3])

def p_setexpr_difference(t):
    '''setexpr : setexpr MINUS setexpr'''
    t[0] = t[1].difference(t[3])

def p_setexpr_parenth(t):
    '''setexpr : LPAREN setexpr RPAREN'''
    t[0] = t[2]

def p_setexpr_named(t):
    '''setexpr : ID'''
    global predicates
    t[0] = predicates[t[1]]

# Error rule

def p_error(t):
    print("Syntax error at '%s'" % t.value)
    print("On line " + str(t.lexer.lineno) + " in structure specification")
    raise StructureSyntaxError

# Build the parser with the Ply package

import ply.yacc as yacc
parser = yacc.yacc()

# Read the whole input file, and parse it

def parseStructFile(filename):
    global predicates
    global predicate_arities
    global constants
    global universe

    print("Parsing '" + filename + "'")

    predicates = dict()
    predicate_arities = dict()
    constants = dict()
    universe = []

    with open(filename, 'r') as f:
        allinput = f.read()
        result = parser.parse(allinput,lexer=structlexer)
    return (universe,predicates,predicate_arities,constants)
