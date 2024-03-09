
# Run a test suite to see how PDB heuristics behave
#
# The tests assess the correctness of NpuzzlePDB.py
# 8-puzzle is solved with A*.
# If you don't have your own A*, replace all 'astar' by 'GBFS' and
# comment out the importing of 'astar'.

from Npuzzle import Npuzzle
from NpuzzlePDB import makePDBheuristic, makePDBheuristic2
from GBFS import GBFS
#from astar import astar

goal8puzzle = Npuzzle(3,3,content = [[1,2,3],[4,5,6],[7,8,0]])
print("GOAL STATE:",end='')
goal8puzzle.show()

# Function to test whether a state is the goal state

goalTest8 = lambda s : s == goal8puzzle

# The Heuristics:

# The trivial admissible heuristic h=0

heur0 = lambda s : 0

# Heuristics with different PDBs

heur1 = makePDBheuristic(goal8puzzle,{1,2})
heur2 = makePDBheuristic(goal8puzzle,{1,2,3})
heur3 = makePDBheuristic2(goal8puzzle,{1,2},{4,5})
heur4 = makePDBheuristic2(goal8puzzle,{4,5,6},{6,7,8})
heur5 = makePDBheuristic2(goal8puzzle,{3,4,5},{6,7,8})
heur6 = makePDBheuristic2(goal8puzzle,{1,2,3,4},{5,6,7,8})

# Test cases to make sure your code is working correctly:

testState0 = Npuzzle(3,3,content =[[1,2,3],[4,5,0],[7,8,6]])
testState1 = Npuzzle(3,3,content =[[3,2,1],[6,5,4],[0,7,8]])
testState2 = Npuzzle(3,3,content =[[8,6,7],[2,5,4],[3,0,1]]) # solution 31 actions
testState3 = Npuzzle(3,3,content =[[6,4,7],[8,5,0],[3,2,1]]) # solution 31 actions
# Values from heuristics 1 to 6
estim0 = [0,0,0,1,1,1]
estim1 = [4,8,8,8,10,18]
estim2 = [6,10,10,9,17,23]
estim3 = [6,10,8,9,15,23]

TESTS = [(0,testState0,estim0),(1,testState1,estim1),(2,testState2,estim2),(3,testState3,estim3)]

algorithm = GBFS
#algorithm = astar

for i,s,e in TESTS:
    print("==== TEST CASE " + str(i),end=' ============================')
    s.show()
    e2 = [ h(s) for h in [heur1,heur2,heur3,heur4,heur5,heur6] ]
    if e == e2:
        print("Lower bounds CORRECT: ",end='')
    else:
        print("Lower bounds INCORRECT: ",end='')
        for i in e2:
            print(str(i),end=" ")
        print(" should be: ",end='')
    for i in e:
        print(str(i),end=" ")
    print()
    plan = algorithm(s,goalTest8,heur6)

# Solve a number of randomly generated initial configurations

print()
print("Randomized initial configurations: ==============================")
print()

for i in range(0,5):

    # Produce a starting configuration by shuffling the goal configuration
    # until it is solvable.
    # Not all configurations are solvable! See https://en.wikipedia.org/wiki/15_puzzle

    init8puzzle = goal8puzzle.copy()
    init8puzzle.shuffle()
    while not init8puzzle.solvable(goal8puzzle):
        init8puzzle.shuffle()

    #init8puzzle.show()

    # Run A* with all of the heuristics
    # Observe how the runtimes and number of visited states decrease with
    # more informative heuristics!

    plan = algorithm(init8puzzle,goalTest8,heur0)
    plan = algorithm(init8puzzle,goalTest8,heur1)
    plan = algorithm(init8puzzle,goalTest8,heur2)
    plan = algorithm(init8puzzle,goalTest8,heur3)
    plan = algorithm(init8puzzle,goalTest8,heur4)
    plan = algorithm(init8puzzle,goalTest8,heur5)
    plan = algorithm(init8puzzle,goalTest8,heur6)
    print("----")
    #for a in plan:
    #    print(a,end=' ')
    # print("")
