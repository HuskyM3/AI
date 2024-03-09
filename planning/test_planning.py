from planning import findPlan
from logic import ATOM, AND, OR, NOT, IMPL, EQVI
from z3 import Bool

def test_planning():

    allStateVars = ["x0","x1","x2"]

    # Current state variables with time tag 0

    x0 = ATOM( ("x0",0) )
    x1 = ATOM( ("x1",0) )
    x2 = ATOM( ("x2",0) )

    # Next state variables with time tag 1

    x0n = ATOM( ("x0",1) )
    x1n = ATOM( ("x1",1) )
    x2n = ATOM( ("x2",1) )

    # Source and target states

    source1 = AND([x0,x1,x2])
    target1 = AND([NOT(x0),NOT(x1),NOT(x2)])

    source2 = AND([NOT(x0),NOT(x1),NOT(x2)])
    target2 = AND([x0,x1,x2])

    source3 = AND([NOT(x0),x1,NOT(x2)])
    target3 = AND([NOT(x0),NOT(x1),x2])

    sourcestargets = [(source1,target1),(source2,target2),(source3,target3)]

    # Transition relation with two alternative changes:
    #   Rotate x0 -> x1, x1 -> x2, x2 -> x0
    #   Toggle x0 (from false to true, or from true to false)

    rotate = AND([EQVI(x0,x1n),EQVI(x1,x2n),EQVI(x2,x0n)])
    toggle0 = AND([EQVI(x0,NOT(x0n)),EQVI(x1,x1n),EQVI(x2,x2n)])
    relation1name = "rotate or toggle0"
    relation1 = OR([rotate,toggle0])

    # Transition relation with three alternative changes:
    #   toggle x0, toggle x1 or toggle x2

    toggle0 = AND([EQVI(NOT(x0),x0n),EQVI(x1,x1n),EQVI(x2,x2n)])
    toggle1 = AND([EQVI(x0,x0n),EQVI(NOT(x1),x1n),EQVI(x2,x2n)])
    toggle2 = AND([EQVI(x0,x0n),EQVI(x1,x1n),EQVI(NOT(x2),x2n)])
    relation2name = "Toggle any bit"
    relation2 = OR([toggle0,toggle1,toggle2])

    relations = [(relation1name,relation1),(relation2name,relation2)]

    MAXLEN = 10

    # Now test all alternative transition relations with the
    # same source and target formulas, to get from 000 to 111.

    for relationname,relation in relations:

        for source,target in sourcestargets:

            print("\nTEST CASE: " + relationname + "\n")

            result = findPlan(source,relation,target,MAXLEN)

            if result == None:
                print("No solutions of length <= " + str(MAXLEN) + " exist.")
            else:
                resultlen,assignment = result
                print("Solution of length " + str(resultlen) + " found.")

                # Display the state sequence:

                for t in range(0,resultlen+1):
                    print("Time " + str(t) + ": ",end='')
                    for x in allStateVars:
                        print(x + "=",end='')
                        if assignment[Bool(x + "@" + str(t))]:
                            print("1 ",end='')
                        else:
                            print("0 ",end='')
                    print("")

test_planning()
