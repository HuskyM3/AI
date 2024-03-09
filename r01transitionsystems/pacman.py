#!/usr/bin/python3

# NOTE: It is recommended to only add the missing code
# in places marked with comments ###
#
# NOTE 2: Do not change the name of the class or the methods, as
# the automated grader relies on the names.

import time
import queue

# Creating a grid for the Pac-Man to wander around.
# The grid is given as a list of string, e.g.
# [".......",
#  ".XXX.X.",
#  ".XXX...",
#  ".XXX.X.",
#  ".....X.",
#  ".XXXXX.",
#  "......."]
# Here the important information is the size of the grid,
# in Y direction the number of string, and in the X direction
# the length of the strings, and whether there is X in
# a grid cell. Pac-Man can enter any cell that is not a wall
# cell marked with X.
# The bottom left cell is (0,0). Cells outside the explicitly
# stated grid are all wall cells.

class PacManGrid:
    def __init__(self,grid):
        self.grid = grid
        self.xmax = len(grid[0]) - 1
        self.ymax = len(grid) - 1

    # Test whether the cell (x,y) is wall.

    def occupied(self,x,y):
        if x < 0 or y < 0 or x > self.xmax or y > self.ymax:
            return True
        s = self.grid[self.ymax-y]
        return (s[x] == 'X')

# State space search problems are represented in terms of states.
# For each state there are a number of actions that are applicable in
# that state. Any of the applicable actions will produce a successor
# state for the state. To use a state space in search algorithms, we
# also need functions for producing a hash value for a state
# (the function hash) and for testing equality of two states.
#
# In this exercise we represent states as Python classes with the
# following components.
#
#   __init__    To create a state (a starting state for search)
#   __repr__    To construct a string that represents the state
#   __hash__    Hash function for states
#   __eq__      Equality for states
#   successors  Returns a list [(a1,s1),...,(aN,sN)] where each si
#               is the successor state when action ai is taken.
#               Here the name ai of an action is a string.

# The state of the Pac-Man (given a grid) consists of
# three components:
# x: the X coordinate 0..self.grid.xmax
# y: the Y coordinate 0..self.grid.ymax
# d: the direction "N", "S", "E", "W" Pac-Man is going
# Based on this information, the possible successor states
# of (x,y,d) are computed by 'successors'.

class PacManState:

    # Creating a state:
    
    def __init__(self,x,y,direction,grid):
        self.x = x
        self.y = y
        self.d = direction
        self.grid = grid

    # Construct a string representing a state.

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + self.d + ")"

    # The hash function for states, mapping each state to an integer

    def __hash__(self):
        return self.x+(self.grid.xmax+1)*self.y

    # Equality for states

    def __eq__(self,other):
        return (self.x == other.x) and  (self.y == other.y) and  (self.d == other.d)

    # All successor states of a state

    def successors(self):
### Implement this function (mine is 67 lines, w/ 4 aux functions)
### You can come up with your own names for the different move
        successors = []
        # Check for forward move
        if not self.grid.occupied(*self.next_position(self.d)):
            successors.append(("Forward", PacManState(*self.next_position(self.d), self.d, self.grid)))

        # Check for left and right turns
        left_dir = self.turn_direction(self.d, "left")
        right_dir = self.turn_direction(self.d, "right")
        #print(left_dir)
        #print(right_dir)

        #print(self.grid.occupied(*self.next_position(left_dir)))

        if not self.grid.occupied(*self.next_position(left_dir)):
            new_x, new_y = self.next_position(left_dir)
            successors.append(("Turn Left", PacManState(new_x, new_y, left_dir, self.grid)))

        if not self.grid.occupied(*self.next_position(right_dir)):
            new_x, new_y = self.next_position(right_dir)
            successors.append(("Turn Right", PacManState(new_x, new_y, right_dir, self.grid)))

        
        
        # Perform U-turn and move forward if possible
        u_turn_dir = self.turn_direction(self.d, "u-turn")
        new_x, new_y = self.next_position(u_turn_dir)
        #print(new_x, new_y)
        #print(self.grid.occupied(new_x, new_y))
        if not self.grid.occupied(new_x, new_y) and self.grid.occupied(*self.next_position(left_dir)) and self.grid.occupied(*self.next_position(right_dir)) and self.grid.occupied(*self.next_position(self.d)):
            successors.append(("U-Turn and Move", PacManState(new_x, new_y, u_turn_dir, self.grid)))

        #print(successors)
       # print(PacManState(0,0, 'N',  self.grid))

        return successors

    def next_position(self, direction):
        if direction == "N":
            return (self.x, self.y + 1)
        elif direction == "S":
            return (self.x, self.y - 1)
        elif direction == "E":
            return (self.x + 1, self.y)
        elif direction == "W":
            return (self.x - 1, self.y)

    def turn_direction(self, current_direction, turn):
        directions = ["N", "E", "S", "W"]
        idx = directions.index(current_direction)
        if turn == "left":
            return directions[(idx - 1) % 4]
        elif turn == "right":
            return directions[(idx + 1) % 4]
        elif turn == "u-turn":
            return directions[(idx + 2) % 4]
