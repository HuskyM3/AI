
# 8-Puzzle, 15-Puzzle generalized to N X M Puzzle

import random

class Npuzzle:

    def __init__(self,N,M,content = None):
        if content == None:
            self.grid = [ [ 0 for n in range(0,N) ] for m in range(0,M) ]
        else:
            self.grid = content

    # Equality for puzzle states

    def __eq__(self,other):
        for y in range(0,len(self.grid)):
            if self.grid[y] != other.grid[y]:
                return False
        return True

    # Order puzzle states lexicographically

    def __lt__(self,other):
        for y in range(0,len(self.grid)):
            for x in range(0,len(self.grid[0])):
                if self.grid[y][x] < other.grid[y][x]:
                    return True
                if self.grid[y][x] > other.grid[y][x]:
                    return False
        return False

    # Map every state to an integer

    def __hash__(self):
        ints = []
        for row in self.grid:
            ints.extend(row)
        h = 0
        for i in ints:
            h = ((h << 1) ^ i) & ((1 << 20) - 1)
        return h

    # Printable representation of puzzle states

    def __repr__(self):
        return "---\n" + '\n'.join([ "".join([ str(i) for i in row]) for row in self.grid]) + "\n---"

    # Make a copy that does not share any lists

    def copy(self):
        new = Npuzzle(len(self.grid[0]),len(self.grid),content=[ c.copy() for c in self.grid ])
        return new

    # Abstract the state by removing some of the tiles

    def abstract(self,tilesToKeep):
        s = self.copy()
        for row in s.grid:
            for x in range(0,len(row)):
                if row[x] not in tilesToKeep:
                    row[x] = 0
        return s

    # Transpose the grid

    def transpose(self):
        for y in range(0,len(self.grid)):
            for x in range(y+1,len(self.grid[0])):
                tmp = self.grid[y][x]
                self.grid[y][x] = self.grid[x][y]
                self.grid[x][y] = tmp

    # Randomly shuffle the grid by shuffling all rows and transposing it

    def shuffle(self):
        for i in range(0,5):
            for y in range(0,len(self.grid)):
                random.shuffle(self.grid[y])
            self.transpose()

    # Show grid

    def show(self):
        print("")
        for y in range(0,len(self.grid)):
            print(" ",end='')
            for x in range(0,len(self.grid[0])):
                if self.grid[y][x] > 0:
                    print(str(self.grid[y][x]),end='')
                else:
                    print(".",end='')
            print("")

    # All possible moves for non-0 tiles

    def successors(self):

        succs = []

        # Go through possible moves to 0-cells

        for y in range(0,len(self.grid)):
           for x in range(0,len(self.grid[0])):

               # Not a 0-cell!

               if self.grid[y][x] > 0:
                   continue

               # Is cell at y-1 a 0-cell?

               if y > 0 and self.grid[y-1][x] > 0:
                   new = self.copy()
                   new.grid[y][x] = new.grid[y-1][x]
                   new.grid[y-1][x] = 0
                   succs.append( ("down" + str(new.grid[y][x]),new,1) )
           
               # Is cell at y+1 a 0-cell?

               if y < len(self.grid) -1 and self.grid[y+1][x] > 0:
                   new = self.copy()
                   new.grid[y][x] = new.grid[y+1][x]
                   new.grid[y+1][x] = 0
                   succs.append( ("up" + str(new.grid[y][x]),new,1) )
           
               # Is cell at x-1 a 0-cell?

               if x > 0 and self.grid[y][x-1] > 0:
                   new = self.copy()
                   new.grid[y][x] = new.grid[y][x-1]
                   new.grid[y][x-1] = 0
                   succs.append( ("left" + str(new.grid[y][x]),new,1) )
           
               # Is cell at x+1 a 0-cell?

               if x < len(self.grid[0]) -1 and self.grid[y][x+1] > 0:
                   new = self.copy()
                   new.grid[y][x] = self.grid[y][x+1]
                   new.grid[y][x+1] = 0
                   succs.append( ("right" + str(new.grid[y][x]),new,1) )

        return succs

    # Test if there is a solution from state to a given goal state

    def parity(self):
        tiles = [ x for x in sum(self.grid,[]) if x > 0 ]
        parity0 = [ tiles[i] > tiles[j] for i in range(0,len(tiles)-1) for j in range(i+1,len(tiles)) ]
        parity1 = len([ x for x in parity0 if x == True ])
        parity = parity1 % 2
        return parity

    def solvable(self,goalstate):
        return (self.parity() == goalstate.parity())
