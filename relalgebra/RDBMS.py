
#
# A simple RDMBS that uses Relational Algebra (not SQL) as the query language.
#
#
# A table is represented as a pair of
# - A set of column names
# - Rows as a list of dictionaries, each mapping a column name to a value
#
# Operations
#   Union of tables (possible if the columns are the same)
#   Natural join
#   Selection
#   Projection
#   Division
#   Difference (possible if the columns are the same)
#   Renaming of the columns

# From a list of rows make a list of rows that has no duplicates.

def removeDuplicateRows(rows):
    result = []
    for row in rows:
        if row not in result:
            result.append(row)
    return result

# Create a dictionary that represents one row in a table.

def makeRow(columnNames,rowData):
    def addToDict(cNames,rData,row):
        if len(cNames) == 0:
            return
        colName = cNames[0]
        data = rData[0]
        row[colName] = data
        addToDict(cNames[1:],rData[1:],row)
    row = dict()
    addToDict(columnNames,rowData,row)
    return row

# Given a list of column names, and a list of lists of column data (data
# in the same order as the column names), create a table.

def makeTable(columnNames,rows):
    return (set(columnNames),[ makeRow(columnNames,row) for row in rows ])

def tableColumns(table):
    return ",".join(table[0])

# Union of two tables (columns must be the same)

def relUnion(table1,table2):
    if table1[0] != table2[0]:
        print("Union of tables with different columns: " + ",".join(table1[0]) + " vs. " + ",".join(table2[0]))
        exit(1)
    table3 = (table1[0],removeDuplicateRows(table1[1] + table2[1]))
    return table3

# Difference of two tables (columns must be the same)

def relDifference(table1,table2):
    if table1[0] != table2[0]:
        print("ERROR: Difference of tables with different columns: " + ",".join(table1[0]) + " vs. " + ",".join(table2[0]))
        exit(1)
    table3 = (table1[0],[ row for row in table1[1] if row not in table2[1] ])
    return table3

# Projection of subset of rows from a table

def relProject(columnNames,table):
    def projectRow(cols,row):
        newRow = dict()
        for col in cols:
            newRow[col] = row[col]
        return newRow
    newCols = columnNames.intersection(table[0])
    return (newCols, removeDuplicateRows([ projectRow(newCols,row) for row in table[1] ]))

# Natural join of two tables

def relNatJoin(table1,table2):
    # Test if two rows agree on the values in 'cols'
    def rowAgree(cols,row1,row2):
        return all(row1[col] == row2[col] for col in cols)

    # Which columns are shared between the two tables?
    jointCols = table1[0].intersection(table2[0])

    # Go through all pairs of rows: create row if the rows agree on the shared columns
    joinedTable = [ dict(row1,**row2) for row1 in table1[1] for row2 in table2[1] if rowAgree(jointCols,row1,row2) ]

    # Join table has all columns in either of the component tables
    allCols = table1[0].union(table2[0])

    return (allCols,removeDuplicateRows(joinedTable))

# Division of two tables:
#   Table 1 has columns C1,...,CN
#   Table 2 has subset of columns, C1,...,CM where M < N
# The result is rows from Table 1 projected to CM+1,...,CN
# so that the row together with every row from Table 2
# is contained in Table 1.

def relDivision(table1,table2):
    #print(table1)
    #print(table2)
    t1exclusive = { col for col in table1[0] if col not in table2[0] }
    result = []
    # Which rows to include in the result?
    for row in table1[1]:
        row0 = dict()
        # row0 is row limited to columns not in table2
        for col in t1exclusive:
            row0[col] = row[col]
        # row0 concatenated with every row in table2 is in table1?
        if all( dict(row0,**row2) in table1[1] for row2 in table2[1] ):
            result.append(row0)
    return (t1exclusive,removeDuplicateRows(result))

# Renaming of columns, with renaming expressed as a dictionary

def relRename(renaming,table):
    oldCols = table[0]
    # New column name: if defined, use renaming, otherwise use old name
    def newname(colName):
        if colName in renaming:
            return renaming[colName]
        else:
            return colName
    # rename a row
    def rowRename(row):
        newRow = dict()
        for col in oldCols:
            newRow[newname(col)] = row[col]
        return newRow
    return ({ newname(colName) for colName in table[0]}, [ rowRename(row) for row in table[1]])

# Boolean conditions on rows, to be used with selection.

class cAnd:
    def __init__(self,expr1,expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def __str__(self):
        return "(" + str(self.expr1) + " AND " + str(self.expr2) + ")"
    def satisfies(self,row):
        return self.expr1.satisfies(row) and self.expr2.satisfies(row)

class cOr:
    def __init__(self,expr1,expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def __str__(self):
        return "(" + str(self.expr1) + " OR " + str(self.expr2) + ")"
    def satisfies(self,row):
        return self.expr1.satisfies(row) or self.expr2.satisfies(row)

class cNot:
    def __init__(self,expr):
        self.expr = expr
    def __str__(self):
        return "(NOT " + str(self.expr) + ")"
    def satisfies(self,row):
        return not self.expr.satisfies(row)

# Atomic Boolean expressions: equality and (numeric) relations

class cEQ:
    def __init__(self,expr1,expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def __str__(self):
        return "(" + str(self.expr1) + " == " + str(self.expr2) + ")"
    def satisfies(self,row):
        return self.expr1.eval(row) == self.expr2.eval(row)

class cGT:
    def __init__(self,expr1,expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def __str__(self):
        return "(" + str(self.expr1) + " > " + str(self.expr2) + ")"
    def satisfies(self,row):
        return self.expr1.eval(row) > self.expr2.eval(row)

class cGEQ:
    def __init__(self,expr1,expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def __str__(self):
        return "(" + str(self.expr1) + " >= " + str(self.expr2) + ")"
    def satisfies(self,row):
        return self.expr1.eval(row) >= self.expr2.eval(row)

# Values: columns, constants and arithmetic expressions

class cCOL:
    def __init__(self,colName):
        self.name = colName
    def __str__(self):
        return self.name
    def eval(self,row):
        return row[self.name]
        
class cCONST:
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return str(self.value)
    def eval(self,row):
        return self.value
        
class cPLUS:
    def __init__(expr1,expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def __str__(self):
        return "(" + str(self.expr1) + " + " + str(self.expr2) + ")"
    def eval(self,row):
        return self.expr1.eval(row) + self.expr2.eval(row)

class cMINUS:
    def __init__(expr1,expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def __str__(self):
        return "(" + str(self.expr1) + " - " + str(self.expr2) + ")"
    def eval(self,row):
        return self.expr1.eval(row) - self.expr2.eval(row)

class cTIMES:
    def __init__(expr1,expr2):
        self.expr1 = expr1
        self.expr2 = expr2
    def __str__(self):
        return "(" + str(self.expr1) + " * " + str(self.expr2) + ")"
    def eval(self,row):
        return self.expr1.eval(row) * self.expr2.eval(row)

# LT, LEQ and NEQ reduced to GT, GEQ and EQ

def cNEQ(e1,e2):
    return rNOT(cEQ(e2,e1))

def cLT(e1,e2):
    return cGT(e2,e1)

def cLEQ(e1,e2):
    return cGEQ(e2,e1)

# Selection of a subset of rows in a table

def relSelect(condition,table):
    return (table[0],[ row for row in table[1] if condition.satisfies(row) ])

# Show table

def printTable(table):
    columns = sorted(list(table[0]))
    if len(columns) == 0:
        print("EMPTY TABLE")
        return
    for c in columns:
        print("===============",end='')
    print("")
    for c in columns:
        print("{:<15}".format(c),end='')
    print("")
    for c in columns:
        print("---------------",end='')
    print("")
    def printRow(columns,row):
        if len(columns) == 0:
            print("")
        else:
            print("{:<15}".format(str(row[columns[0]])),end='')
            printRow(columns[1:],row)
    for row in table[1]:
        printRow(columns,row)
    print("")

# Sample tables

if __name__ == "__main__":
    TABLE1 = makeTable(["COL1","COL2"],[["John",2],["Jill",3],["John",10]])
    TABLE2 = makeTable(["COL2","COL3","COL4"],[[2,"A",4],[3,"B",6],[3,"C",7],[4,"C",8]])
    TABLE3 = relNatJoin(TABLE1,TABLE2)
    TABLE4 = relProject({"COL1","COL2"},TABLE3)
    printTable(TABLE3)
    printTable(TABLE4)
    printTable(relSelect(cLT(cCOL("COL2"),cCONST(3)),TABLE4))
