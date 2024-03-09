#!/usr/bin/python3

from logic import *

# Auxiliary functions

# Conjunction AND(f1,AND(f2,AND(f3,...))) from a list [f1,f2,f3,...]

def chainAND(l):
  if l == []:
    return TRUE()
  elif len(l) == 1:
    return l[0]
  else:
    return AND(l[0],chainAND(l[1:]))

# Tests

A = ATOM("A")
B = ATOM("B")
C = ATOM("C")
D = ATOM("D")
E = ATOM("E")
F = ATOM("F")
G = ATOM("G")
H = ATOM("H")
I = ATOM("I")
J = ATOM("J")
K = ATOM("K")
L = ATOM("L")
M = ATOM("M")
N = ATOM("N")
O = ATOM("O")
P = ATOM("P")
Q = ATOM("Q")
R = ATOM("R")
S = ATOM("S")
T = ATOM("T")
U = ATOM("U")
V = ATOM("V")
W = ATOM("W")
X = ATOM("X")
Y = ATOM("Y")
Z = ATOM("Z")

# Test cases for truthValue:

if FALSE().truthValue([]) == False:
  print ("truthValue for FALSE seems to work OK!")
else:
  print ("FAIL: truthValue for FALSE!")

if TRUE().truthValue([]) == True:
  print ("truthValue for TRUE seems to work OK!")
else:
  print ("FAIL: truthValue for FALSE!")

if A.truthValue([]) == False and A.truthValue(["A"]) == True:
  print ("truthValue for ATOM seems to work OK!")
else:
  print ("FAIL: truthValue for ATOM!")

if NOT(A).truthValue([]) == True and NOT(A).truthValue(["A"]) == False:
  print ("truthValue for NOT seems to work OK!")
else:
  print ("FAIL: truthValue for NOT!")

if AND(A,B).truthValue([]) == False and AND(A,B).truthValue(["A"]) == False and AND(A,B).truthValue(["B"]) == False and AND(A,B).truthValue(["A","B"]) == True:
  print ("truthValue for AND seems to work OK!")
else:
  print ("FAIL: truthValue for AND!")

if OR(A,B).truthValue([]) == False and OR(A,B).truthValue(["A"]) == True and OR(A,B).truthValue(["B"]) == True and OR(A,B).truthValue(["A","B"]) == True:
  print ("truthValue for OR seems to work OK!")
else:
  print ("FAIL: truthValue for OR!")

if AND(AND(A,B),C).truthValue([]) == False and AND(AND(A,B),C).truthValue(["A","B","C"]) == True:
  print ("truthValue for nested connectives seems to work OK!")
else:
  print ("FAIL: truthValue for nested ANDs!")

# Simple tests to see if 'satisfiable' works correctly:

if satisfiable(AND(A,B)) != False:
  print("Test 1 OK")
else:
  print("Test 1 FAILS")

#print(satisfiable(AND(A,B)) )

if satisfiable(AND(A,NOT(A))) != False:
  print("Test 2 FAILS")
else:
  print("Test 2 OK")

#print( (AND(A,A)).truthValue(['A']) )
#print( (AND(A,NOT(A))).truthValue(['']) )
#print(satisfiable(AND(A,NOT(A))))
#print(AND(AND(A,NOT(B)),C).truthValue(["A", "C"]))

if satisfiable(chainAND([A,OR(B,C),IMPL(B,NOT(A)),IMPL(C,NOT(A))])) != False:
  print("Test 3 FAILS")
else:
  print("Test 3 OK")

if satisfiable(AND(A,B)) != False:
  print("Test 4 OK")
else:
  print("Test 4 FAILS")

###
### The party example from the lecture
###


PARTY1 = chainAND([IMPL(NOT(B),NOT(A)),
                   OR(NOT(B),NOT(C)),
                   OR(C,D),
                   IMPL(AND(A,E),D),
                   NOT(AND(B,D))])

print("Solution to PARTY1: ",end='')
print(satisfiable(PARTY1))

# More complicated party with more guests and constraints

PARTY2 = chainAND([IMPL(NOT(B),NOT(A)),
                   OR(NOT(B),NOT(C)),
                   OR(C,D),
                   IMPL(AND(A,E),D),
                   NOT(AND(B,D)),
                   OR(E,OR(F,OR(G,H))),
                   IMPL(OR(H,I),OR(NOT(J),NOT(K))),
                   IMPL(AND(I,K),IMPL(L,M))
])

print("Solution to PARTY2: ",end='')
print(satisfiable(PARTY2))

# An even more complicated party

PARTY3 = chainAND([IMPL(NOT(B),NOT(A)),
                   OR(NOT(B),NOT(C)),
                   OR(C,D),
                   IMPL(AND(A,E),D),
                   NOT(AND(B,D)),
                   OR(E,OR(F,OR(G,H))),
                   IMPL(OR(H,I),OR(NOT(J),NOT(K))),
                   IMPL(AND(I,K),IMPL(L,M)),
                   EQVI(OR(M,NOT(N)),IMPL(O,P)),
                   IMPL(NOT(B),EQVI(P,OR(Q,NOT(R)))),
                   OR(R,OR(NOT(S),NOT(T)))
])

# COMMENT: The calls to 'satisfiable' have been commented out because
# you might run out of memory. Try carefully.

#print("Solution to PARTY3: ",end='')
#print(satisfiable(PARTY3))

PARTY4 = chainAND([IMPL(NOT(B),NOT(A)),
                   OR(NOT(B),NOT(C)),
                   OR(C,D),
                   IMPL(AND(A,E),D),
                   NOT(AND(B,D)),
                   OR(E,OR(F,OR(G,H))),
                   IMPL(OR(H,I),OR(NOT(J),NOT(K))),
                   IMPL(AND(I,K),IMPL(L,M)),
                   EQVI(OR(M,NOT(N)),IMPL(O,P)),
                   IMPL(NOT(B),EQVI(P,OR(Q,NOT(R)))),
                   OR(R,OR(NOT(S),NOT(T))),
                   OR(NOT(U),NOT(V)),
                   IMPL(Z,NOT(Y)),
                   IMPL(W,OR(X,A))
])

#print("Solution to PARTY4: ",end='')
#print(satisfiable(PARTY4))

###
### The 3-bit Binary Adder from the lecture
###

A0 = ATOM("A0")
A1 = ATOM("A1")
A2 = ATOM("A2")
B0 = ATOM("B0")
B1 = ATOM("B1")
B2 = ATOM("B2")
C0 = ATOM("C0")
C1 = ATOM("C1")
C2 = ATOM("C2")
S0 = ATOM("S0")
S1 = ATOM("S1")
S2 = ATOM("S2")

def XOR(f1,f2):
  return EQVI(f1,NOT(f2))

ADDER = chainAND([EQVI(S0,XOR(A0,B0)),
                  EQVI(C0,AND(A0,B0)),
                  EQVI(S1,XOR(C0,XOR(A1,B1))),
                  EQVI(C1,OR(AND(C0,XOR(A1,B1)),AND(A1,B1))),
                  EQVI(S2,XOR(C1,XOR(A2,B2))),
                  EQVI(C2,OR(AND(C1,XOR(A2,B2)),AND(A2,B2)))])

### Test cases for the adder:

print("Adder with inputs 111B+111B (7+7) : ",end='')
print(satisfiable(chainAND([ADDER,A0,A1,A2,B0,B1,B2])))

print("Adder with output 1110B=14: ",end='')
print(satisfiable(chainAND([ADDER,NOT(S0),S1,S2,C2])))

print("Adder with output 1010B=10: ",end='')
print(satisfiable(chainAND([ADDER,S0,NOT(S1),S2,NOT(C2)])))

print("Adder with inputs 7+0= : ",end='')
print(satisfiable(chainAND([ADDER,A0,A1,A2,NOT(B0),NOT(B1),NOT(B2)])))

print("Adder inputs 0+7= : ",end='')
print(satisfiable(chainAND([ADDER,NOT(A0),NOT(A1),NOT(A2),B0,B1,B2])))

print("Adder with equal inputs and non-zero output: ",end='')
print(satisfiable(chainAND([ADDER,EQVI(A0,B0),EQVI(A1,B1),EQVI(A2,B2),OR(S0,OR(S1,S2))])))

### Test cases for logicalConsequence

if logicalConsequence(A,A) == True:
  print("Test 5 OK")
else:
  print("Test 5 FAILS")

if logicalConsequence(AND(A,B),A) == True:
  print("Test 6 OK")
else:
  print("Test 6 FAILS")

if logicalConsequence(A,OR(A,B)) == True:
  print("Test 7 OK")
else:
  print("Test 7 FAILS")

if logicalConsequence(AND(A,AND(B,C)),AND(A,C)) == True:
  print("Test 8 OK")
else:
  print("Test 8 FAILS")

if logicalConsequence(IMPL(A,B),IMPL(NOT(B),NOT(A))) == True:
  print("Test 9 OK")
else:
  print("Test 9 FAILS")

if logicalConsequence(OR(A,B),AND(A,B)) == False:
  print("Test 10 OK")
else:
  print("Test 10 FAILS")

if logicalConsequence(OR(A,B),OR(A,OR(B,C))) == True:
  print("Test 11 OK")
else:
  print("Test 11 FAILS")
