#!/usr/bin/python3

#
# Author: Jussi Rintanen, (C) Aalto University
# Only for student use on the Aalto course CS-E4800/CS-EJ4801.
# Do not redistribute.
#

#
# Functions in classes representing state space search problems:
#   __init__    To create a state (a starting state for search)
#   __repr__    To construct a string that represents the state
#   __hash__    Hash function for states
#   __eq__      Equality for states
#   successors  Returns [(a1,s1,c1),...,(aN,sN,cN)] where each si is
#               the successor state when action called ai is taken,
#               and ci is the associated cost.
#               Here the name ai of an action is a string.

import time
import queue

DEBUG=False
#DEBUG=True

def GBFS(initialstate,goaltest,h):

    starttime = time.process_time()
    
    visited = dict() # dictionary (hash table) for holding visited states
    predecessor = dict() # dictionary (hash table) for holding predecessors
        
    def getPath(s):
        if s == initialstate:
            return [initialstate]
        else:
            states = getPath(predecessor[s])
            return states + [s]

    Q = queue.PriorityQueue(maxsize=0)

    if DEBUG:
        print("GBFS: Initial state is " + str(initialstate))
    Q.put( (h(initialstate),(initialstate,[])) ) # Insert the initial state in the queue

    statVisits = 0
    statExpansions = 0

    while not Q.empty():
        hvalue,data = Q.get() # Highest priority state from the queue
        state,acts = data
        if DEBUG:
            print("Expanding state " + str(state))
        statExpansions += 1
        for aname,s,cost in state.successors(): # Go through all successors of state
            if s not in visited: # Is state in the dictionary?
                predecessor[s] = state
                if DEBUG:
                    print("New state " + str(s) + " of h-value " + str(h(s)))
                statVisits += 1
                if goaltest(s):
                    endtime = time.process_time()
                    print(str(statExpansions) + " expansions " + str(statVisits) + " visits " + str(len(acts + [aname])) + " actions " + " runtime ",str(endtime-starttime))
                    return acts + [aname]
                visited[s] = 1
                Q.put( (h(s),(s,acts + [aname] )) )
    print("All states visited, goals not reached")
