#!/usr/bin/python3

from pacman import *

# The following is a standard breadth-first search algorithm, which
# first finds all states one step from the initial state, then all
# states two steps from the initial states, and so on.
# It is guaranteed to find the shortest sequence  of actions that
# reaches a goal state.

VERBOSE = False

def breadthFirstSearch(initialstate,goaltest):
    statExpansions = 0 # number of expanded states
    statVisits = 0 # number of encountered states

    starttime = time.process_time()
    
    visited = dict() # dictionary (hash table) for holding visited states

    # The first-in-first-out queue for breadth-first search
    Q = queue.Queue(maxsize=0)
    # The pairs (s,p) in the queue consists of
    # s: state for which successors have not yet been generated
    # p: shortest path (list of action names) from initial state to s

    print("Initial state is " + str(initialstate))

    # Insert the initial state & the empty path in the queue
    Q.put( (initialstate,[]) )
    
    while not Q.empty():
        state,path = Q.get() # Next un-expanded state from the queue
        if VERBOSE:
            print("Expanding state " + str(state))
        statExpansions += 1
        for aname,s in state.successors(): # Go through all successors of state
            if s not in visited: # It is a new state
                statVisits += 1
                if goaltest(s): # goaltest decides if it is a goal state
                    endtime = time.process_time()
                    print("Goal state " + str(s) + " reached")
                    print(str(statExpansions) + " expansions, " + str(statVisits) + " visits")
                    print(path + [aname])
                    print("Elapsed time ",str(endtime-starttime))
                    print()
                    return 0
                visited[s] = 1
                Q.put( (s,path + [aname] ) )
                if VERBOSE:
                    print("New state " + str(s) + " with action " + aname)

    # All reachable states visited, no goal states encountered...
    endtime = time.process_time()
    nOfStates = len(visited)
    print("All reachable states generated: total of " + str(nOfStates) + " states")
    print("Elapsed time ",str(endtime-starttime))
    print()
    return nOfStates

# The following code runs the breadth-first search algorithm with
# different initial states and goal states.
# The goal states are represented by an unnamed function that
# returns 'true' if the given state is a goal state.

GRID1 = PacManGrid(["......",
                    ".XX.X.",
                    "......"])
ISTATE1 = PacManState(0,0,"N",GRID1)

# Generate all reachable states
breadthFirstSearch(ISTATE1,lambda state: False)

# Back to 0,0 but not facing North
breadthFirstSearch(ISTATE1,lambda state: (state.x == 0) and (state.y == 0) and (state.d != "N"))

# Another grid
GRID2 = PacManGrid([".......",
                    ".XXX.X.",
                    ".XXX...",
                    ".XXX.X.",
                    ".....X.",
                    ".XXXXX.",
                    "......."])
ISTATE2 = PacManState(0,0,"N",GRID2)

# Generate all reachable states
breadthFirstSearch(ISTATE2,lambda state: False)

# Back to 0,0 but not facing North
breadthFirstSearch(ISTATE2,lambda state: (state.x == 0) and (state.y == 0) and (state.d != "N"))
