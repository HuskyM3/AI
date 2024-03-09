
from RDBMS import relNatJoin, relUnion, relDifference, relDivision, relProject, relSelect, relRename

# Function to add 'n' blanks in front of every line in 'lines'

def INDENT(n,lines):
    blanks = n * " "
    return [ blanks + line for line in lines ]

#
# Relational algebra expressions
#
# The method 'eval' calls the functions in RDBMS.py to evaluate
# the value of the expression, in other words, to query the
# database to obtain the answer to the database query.
#
# The other methods __str__ and prettyprint are for showing
# the expressions. The latter shows the expression nicely
# indented on multiple lines, for readability.

# Table from the database

class RAtable():
    def __init__(self,tablename):
        self.table = tablename
    def __str__(self):
        return self.table
    def prettyprint(self):
        return [str(self)]
    def eval(self,db):
        return db[self.table]

# Parent class for relational algebra's binary operations of two tables 

class RAbinaryOp():
    def __init__(self,expr1,expr2):
        self.expr1 = expr1
        self.expr2 = expr2

# Union

class RAunion(RAbinaryOp):
    def __str__(self):
        return "(" + str(self.expr1) + " UNION " + str(self.expr2) + ")"
    def prettyprint(self):
        pp1 = self.expr1.prettyprint()
        pp2 = self.expr2.prettyprint()
        return INDENT(4,pp1) + ["UNION"] + INDENT(4,pp2)
    def eval(self,db):
        return relUnion(self.expr1.eval(db),self.expr2.eval(db))

# Difference

class RAdifference(RAbinaryOp):
    def __str__(self):
        return "(" + str(self.expr1) + " DIFFERENCE " + str(self.expr2) + ")"
    def prettyprint(self):
        pp1 = self.expr1.prettyprint()
        pp2 = self.expr2.prettyprint()
        return INDENT(4,pp1) + ["DIFFERENCE"] + INDENT(4,pp2)
    def eval(self,db):
        return relDifference(self.expr1.eval(db),self.expr2.eval(db))

# Natural join

class RAnatjoin(RAbinaryOp):
    def __str__(self):
        return "(" + str(self.expr1) + " JOIN " + str(self.expr2) + ")"
    def prettyprint(self):
        pp1 = self.expr1.prettyprint()
        pp2 = self.expr2.prettyprint()
        return INDENT(4,pp1) + ["NATURAL JOIN"] + INDENT(4,pp2)
    def eval(self,db):
        return relNatJoin(self.expr1.eval(db),self.expr2.eval(db))

# Division

class RAdivision(RAbinaryOp):
    def __str__(self):
        return "(" + str(self.expr1) + " DIV " + str(self.expr2) + ")"
    def prettyprint(self):
        pp1 = self.expr1.prettyprint()
        pp2 = self.expr2.prettyprint()
        return INDENT(4,pp1) + ["DIVISION"] + INDENT(4,pp2)
    def eval(self,db):
        #print(self.expr1.eval(db))
        return relDivision(self.expr1.eval(db),self.expr2.eval(db))

# Projection

class RAproject():
    def __init__(self,columns,expr):
        self.columns = columns
        self.expr = expr
    def __str__(self):
        return "PROJECT( {" + ",".join(self.columns) + "}, " + str(self.expr) + ")"
    def prettyprint(self):
        pp = self.expr.prettyprint()
        return ["PROJECT( {" + ",".join(self.columns) + "},"] + INDENT(9,pp) + INDENT(8,[")"])
    def eval(self,db):
        return relProject(self.columns,self.expr.eval(db))

# Renaming

class RArename():
    def __init__(self,renaming,expr):
        self.renaming = renaming
        self.expr = expr
    def __str__(self):
        return "RENAME({" + ",".join([ key + " -> " + self.renaming[key] for key in self.renaming]) + "}, " + str(self.expr) + ")"
    def prettyprint(self):
        pp = self.expr.prettyprint()
        return ["RENAME( {" + ",".join([ key + " -> " + self.renaming[key] for key in self.renaming]) + "},"] + INDENT(8,pp) + INDENT(7,[")"])
    def eval(self,db):
        return relRename(self.renaming,self.expr.eval(db))

# Selection

class RAselect():
    def __init__(self,condition,expr):
        self.condition = condition
        self.expr = expr
    def __str__(self):
        return "SELECT(" + str(self.condition) + ", " + str(self.expr) + ")"
    def prettyprint(self):
        pp = self.expr.prettyprint()
        return ["SELECT( " + str(self.condition) + ","] + INDENT(7,pp) + INDENT(6,[")"])
    def eval(self,db):
        return relSelect(self.condition,self.expr.eval(db))
