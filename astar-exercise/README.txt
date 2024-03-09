A* exercise
-----------

In this programming exercise you will be implementing the A* algorithm.

- Start by copying the file 'template-astar.py' to 'astar.py'; your task is to complete the function 'astar' in that file.

- Read and understand the code.

- Your implementation should go where the TASK comments start.

The code archive also contains a few other files than 'astar.py', no work is needed there, but make sure you read through the code so that you understand the different classes and the task. The files all contain doc-strings which describes their purpose in more detail.

The states and actions used in this exercise are derived from the same base classes as was used in the previous exercise. The planning problem we are applying A* to solve is different than the the moving knights however - this time it is a so called Multi-Agent Path Planning problem. Here multiple 'agents' may move at the same time, creating a potentially huge number of successor states. You can find out more about the problem below and in the file 'mappstate.py'.

Just as with the Breadth First Search function in the previous exercise, astar takes a start state and a goal test function as inputs and should return a plan, that is a list of Action objects.
As such you can, if you wish use the bfs function from that exercise to get a rough idea of what needs to be done.

However, note that astar also takes a heuristic function as input, and uses a PriorityQueue instead of a normal Queue to store the states to be expanded.

Make sure that you do not by mistake implement Greedy Breadth First Search instead of A* (see e.g. the lectures to understand the difference). The former is not guaranteed to find the optimal path, while A* does.

Make sure your A* implementation does not terminate prematurely: after encountering a goal state, you still have to expand all those states that could potentially be part of a still better plan. There is no a priori limit on how many such expansions are needed, nor on how many times a still better plan is found.


Testing the code
----------------

- Some informal examples using the MAPP problem - printing expected cost and rough running times - is run by running astar.py: 'python astar.py'.

- There are a few unit test, including a test for optimality, in test_astar.py: 'python test_astar.py'.

Note
----

- It is worthwhile to consult the algorithm descriptions in both the MyCourses material and in the lecture.

- The algorithm description in the lecture slides uses sets to hold states. However, in practice you will be using a priority queue to represent the OPEN set. If you try to use a set (or list) in your implementation it will be very slow (because finding the lowest f(s) means searching it).

- Don't forget the return statement!


The MAPP problem
----------------

The problem which we will solve using the A* code is a Multi-Agent Path Planning (MAPP) problem.

The basic idea is that several agents (numbered 0-N) is located in a rectangular grid of n rows x m columns. The grid may also contain walls, where no agent may be located.

The problem where your A* code will be employed is to find the cheapest plan for the agents to move from some start locations on the grid to some goal locations.

The rules of this particular MAPP is that
- Agents may only move in the cardinal directions (North, South, East, West).
- Agents may all move at the same time, but
- Two or more Agents can not stand in the same location
- Agents can not 'jump' over each other, but
- Agents may move in 'cycles'
- Agents can not move outside the grid
- Agents can not move into a wall location

For more information see 'mappstate.py'.


Good luck!

