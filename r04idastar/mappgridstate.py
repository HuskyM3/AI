from dataclasses import dataclass # Use dataclass to create hash, eq, and order.
import itertools # For creating combinations.
# Local imports.
import state 
from action import Action
from mappdistance import manhattan

@dataclass(eq=True, order=True, unsafe_hash=True)
class MAPPGridState(state.State):
    """
    This is Multi-Agent Path Planning (MAPP) in rectangular grids.

    The grid consists of rows and columns. Each coordinate location is either
    empty, or contains a wall, or an agent. Agents are numbered 0 ... N-1.
    
    Agents may stay in their location or move N,S,E,W in the grid (but not over
    the 'edge', in to a wall location, or into a space occupied by another 
    agent).
    Crucially, all agents may move simultaneously. See `successors` for more on
    the specifics.

    The cost of a move is the sum of distances for all agents moving.

    Simultaneous movement has the potential to create a huge number of successor
    states, with the potential to overwhelm e.g. BFS. This class is designed as
    an example used with A-star search.

    Attributes
    ----------
    nrows : int > 0
       Number of rows in grid.
    ncols : int > 0
       Number of columns in grid.
    agents : tuple of (int,int) pairs
       Location of all agents (list index i is the location of agent i).
    walls : set of (int,int)
       Location of walls (cells that cannot be entered by an agent).

    Note
    ----
    Ordering and performance : This class is supposed to be used with the A-star
    algorithm, which is based around `queue.PriorityQueue`. PriorityQueue 
    primarily orders its items based on the priority score (lowest first), but
    in the event that two scores are the same it requires the data object to 
    have an order (a __lt__ method). In the case when there are multiple states
    with the same score the running time can be significantly impacted by the
    state to state ordering. This class simply uses `dataclass` to automatically
    create an ordering, which means that there are some configurations 
    (especially with open spaces) when finding a path in one direction (S->G) is
    much slower/faster than the other (G->S). Some specific implementations of
    __lt__ may give a better on-average performance.
    
    See
    ---
    mappdistance.py
       For a couple of simple heuristics.
    astar.py
       For a few examples using astar to solve MAPP problems.
    """

    # Attributes for dataclass
    agents : tuple
    walls : set
    nrows : int
    ncols : int
   
    def __init__(self, locations, nrows = 10, ncols = 10, walls = {}):
        """
        Create new state.
        
        Parameters
        ----------
        See class attributes above.

        Raises
        ------
        ValueError
           If agent locations are on walls, outside the grid, or not unique.
        """
        self.nrows = nrows
        self.ncols = ncols
        self.walls = frozenset(walls)
        # Temporary storage
        agents = []
        # Check input while copying agents
        for (r,c) in locations:
            if (r,c) in self.walls:
                raise ValueError(f"An agent can not be located in a wall {(r,c)}.")
            if r < 0 or r >= self.nrows or c < 0 or c >= self.ncols:
                raise ValueError(f"Agent location {(r,c)} is outside grid.")
            if (r,c) in agents:
                raise ValueError(f"Location {(r,c)} already occupied by an agent.")
            # All good? Add agent
            agents.append((r,c))
        self.agents = tuple(agents)

   
    def apply(self,action):
        """
        Apply an action and return new state.
        
        Parameters
        ----------
        action : Action
           The action to apply. action.source needs to be the same as 
           self.agents for the action to be applicable.

        Returns
        -------
        MAPPGridState
           The resulting state.

        Raises
        ------
        ValueError
           If the action is not applicable.
        """
        if self.agents != action.source:
            raise ValueError("Can only apply action to state with same agents.")
        # Return new state based on self and target locations.
        return MAPPGridState(action.target, self.nrows, self.ncols,
                             walls = self.walls)

    def successors(self):
        """
        Get all possible successor states and associated actions.

        A successor state is possible if all agents move so that there is no
        direct swap of position between any pair of agents, no agent move into
        a wall location or outside the grid, and not more than one agent is
        located at any one position.

        Theory
        ------
        One can define simultaneous moves by agents different ways;
        
        1. The strictest definition requires that every agent is moving to
        an empty cell. Transition from ...12... to ....12.. is not allowed.
        
        2. A looser definition does not allow any cycles in the moves.
        Transition from ...12... to ....12.. is OK
        but transition from ...12... to ...21... is not.

        The definition used here forbids cycles involving 2 agents. But longer cycles are OK,
        for example
        from ..12.. to ..31..
             ..34..    ..42..
        as this does not involve agents jumping over each other.

        Agents may also stand still.

        Our agents move to the 4 cardinal directions N, S, W and E only.
        One could of course allow also the intermediate NE, NW, SE, SW.
        

        Returns
        -------
        list of (Action, MAPPGridState)
           List of actions and new state.
        """
        # This list will store possible target locations for each agent.
        moves = []
        # Go over all agents/locations.
        # The index is the agent id so simply iterate over it.
        for (r,c) in self.agents:
            # Add possible Manhattan moves (north, south, east, west) and no
            # move as a list.
            moves.append([])
            for (dr,dc) in ((0,0),(0,1),(1,0),(0,-1),(-1,0)):
                # Calculate new location.
                (rt,ct) = (r+dr,c+dc)
                # Check if new location is in wall or outside.
                # Do not check move to occupied space just yet.
                if (rt,ct) not in self.walls \
                   and rt >= 0 and ct >=0 \
                   and rt < self.nrows and ct < self.ncols:
                    # Last element is current agent.
                    moves[-1].append((rt,ct))
        # Now we have a list of possible target locations for each agent.
        # As every agent can make one move between one state and the next, the
        # next thing to do is to calculate all possible products of moves,
        # (i.e. all combinations where one move is picked for each agent).
        # If the combination contains no place swaps and no shared locations,
        # it is a valid action.
        succ = []
        for locations in itertools.product(*moves):
            # Now go over each combination of distinct agent ID's
            # Check so no double occupancy, nor
            # swap of places.
            if all(not (locations[i] == locations[j] \
                            or (self.agents[i] == locations[j] \
                                and self.agents[j] == locations[i])) \
                       for i in range(len(self.agents))
                       for j in range(i+1,len(self.agents))):
                # All good; append an action and the new state to the successors.
                # Cost is the sum of Manhattan distance for all moves.
                cost = sum(manhattan(u,v) for (u,v) in zip(self.agents,locations))
                if cost == 0:
                    continue
                succ.append((Action(self.agents,locations, cost),
                            MAPPGridState(locations, nrows = self.nrows,
                                          ncols = self.ncols, walls = self.walls)))
        return succ

    def __str__(self):
        """
        Multi-line text visualization of grid.
        """
        s = ''
        for r in range(self.nrows):
            for c in range(self.ncols):
                if (r,c) in self.agents:
                    s += str(self.agents.index((r,c)))
                elif (r,c) in self.walls:
                    s += '#'
                else:
                    s += '.'
            s += '\n' # End line
        return s


    def create_from_string(mapp_strings):
        """
        Create MAPPGridState from strings.

        Reads each line as a row in grid, and each character as column.
        '#' as wall.
        '.' as empty space.
        Any other character as an agent ID.

        Note that agent id's are sorted and remapped to integers.

        Class method.
        
        Parameters
        ----------
        mapp_strings : list of str

        Returns
        -------
        MAPPGridState
        """
        nrows = len(mapp_strings)
        # Assume the number of columns is constant
        ncols = len(mapp_strings[0])
        walls = []
        agents = {}
        for row,rdata in enumerate(mapp_strings):
            for col,cdata in enumerate(rdata):
                if cdata == '#':
                    walls.append((row,col))
                elif cdata == '.':
                    pass
                else:
                    agents[cdata] = (row,col)
        # Create state, sorting the agent dictionary to make
        # sure the order is right.
        return MAPPGridState([agents[a] for a in sorted(agents)],
                             nrows, ncols,
                             walls = walls)


if __name__ == "__main__":
    # A few examples.
    # Creating state with two agents, agent 0 at (0,0) and agent 1 at (5,4).
    x = MAPPGridState([(0,0), (5,4)], nrows=7, ncols=5)
    # Creating a state with walls.
    y = MAPPGridState([(1,0), (9,9)], walls = {(5,5),(1,1),(7,9)})
    # Create the same state, but parse it.
    z = MAPPGridState.create_from_string(
        ["..........",
         "0#........",
         "..........",
         "..........",
         "..........",
         ".....#....",
         "..........",
         ".........#",
         "..........",
         ".........1"])
         
    print("Some example MAPP states.")
    print("x=")
    print(str(x))
    print("----")
    print("y=")
    print(str(y))
    print("----")
    print("z=")
    print(str(z))
    printf("Moreover, y and z are the same state: {y == z}.")
