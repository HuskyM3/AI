
from action import Action

# Order integer lists

def listLT(l1,l2):
    if len(l1) < len(l2):
        return True
    if len(l1) > len(l2):
        return False
    for i in range(len(l1)):
        if l1[i] < l2[i]:
            return True
        if l1[i] > l2[i]:
            return False
    return False

# Equality of integer lists
    
def listEQ(l1,l2):
    if len(l1) != len(l2):
        return False
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            return False
    return True

def int2char(i):
    if i < 10:
        return str(i)
    return str(chr(i-10+65))
    
def char2int(c):
    if ord('0') <= ord(c) and ord(c) <= ord('9'):
        return ord(c) - ord('0')
    return ord(c) - ord('A') + 10
    
class StackState():

    def __init__(self,stacks):
        self.stacks = stacks

    def __str__(self):
        result = ""
        for x in range(len(self.stacks)):
            result += "."
        result += "\n"
        maxHeight = max([ len(s) for s in self.stacks ])
        for y in range(maxHeight-1,-1,-1):
            for x in range(len(self.stacks)):
                if len(self.stacks[x]) > y:
                    result += int2char(self.stacks[x][y])
                else:
                    result += "."
            result += "\n"
        for x in range(len(self.stacks)):
            result += "="
        result += "\n"
        return result

    def __lt__(self,other):
        for i in range(len(self.stacks)):
            if listLT(self.stacks[i],other.stacks[i]):
                return True
            if listLT(other.stacks[i],self.stacks[i]):
                return False
        return False

    def __eq__(self,other):
        if len(self.stacks) != len(other.stacks):
            return False
        for i in range(len(self.stacks)):
            if not listEQ(self.stacks[i],other.stacks[i]):
                return False
        return True

    def __hash__(self):
        return sum([ n*(i+1)*j+n for j,l in enumerate(self.stacks) for i,n in enumerate(l) ])

    # One successor state obtained with action

    def apply(self,action):
        source,block = action.source
        target = action.target
        newstacks = []
        for x,s in enumerate(self.stacks):
            if x==source:
                # Drop top element from stack
                newstacks.append(s[:-1])
            elif x==target:
                # Add m on top
                newstacks.append(s + [block])
            else:
                # Stack does not change
                newstacks.append(s)
        return StackState(newstacks)

    # The successors are obtained by identifying all
    # blocks that can be moved from stack to stack.

    def successors(self):
        nOfStacks = len(self.stacks)
        movable = []
        for i in range(len(self.stacks)):
            if len(self.stacks[i]) > 0:
                movable.append( (i,self.stacks[i][-1]) )
        # Compute all actions possible
        moves = []
        for i,m in movable:
            for j in range(nOfStacks):
                # move block 'm' from stack i to stack j
                if i == j:
                    continue
                moves.append(Action((i,m),j,1))
        # Construct successor states
        ss = []
        for a in moves:
            s2 = self.apply(a)
            ss.append( (a,s2) )
                
        return ss

    def makeFromStrings(ss):
        stacks = [ [ char2int(c) for c in s ] for s in ss ]
        return StackState(stacks)

# Lower bound on the number of blocks to move
# Blocks in the bottom of a stack in right locations
# do not need to be moved. How many blocks are there
# on top of those, which must be?

def needsToMove(l1,l2):
    for i in range(min(len(l1),len(l2))):
        if l1[i] != l2[i]:
            return len(l1) - i
    if len(l1) > len(l2):
        return len(l1) - len(l2)
    return 0

def computeStackDistance(s1,s2):
    distance = 0
    # How many top elements must move in each stack?
    for x in range(len(s1.stacks)):
        distance = distance + needsToMove(s1.stacks[x],s2.stacks[x])
    # How many pairs of stacks S1 and S2 there are so that
    # a block in S1 has to go to S2, and a block in S2 has to go to S1?
    # Each of these pairs means at least one move to a temporary location.
    for x1 in range(len(s1.stacks)):
        for x2 in range(x1+1,len(s2.stacks)):
            if not set(s1.stacks[x1]).isdisjoint(s2.stacks[x2]) and not set(s1.stacks[x2]).isdisjoint(s2.stacks[x1]):
                distance = distance + 1
#    print("DISTANCE IS " + str(distance))
#    print(str(s1))
#    print(str(s2))
    return distance

def stackDistance(G):
    return lambda s: computeStackDistance(s,G)
