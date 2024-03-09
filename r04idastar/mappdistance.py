"""
Distance heuristics to be used with MAPP states.
See: mappgridstate.py and astar.py
"""
from abc import abstractmethod, ABC
from dataclasses import dataclass


@dataclass
class MAPPHeuristic(ABC):
    """
    Abstract base class for describing heuristic functions h(s) for 2D MAPP.
    """

    # Dataclass attributes
    goal : 'MAPPGridState' # Goal state.
    
    @abstractmethod
    def __call__(self, state):
        """
        Calculates the heuristic from self.goal to `state`.

        Parameters
        ----------
        state : MAPPGridState
           The s in h(s).

        Returns
        -------
        float
           Distance heuristic to goal state.
        """
        pass

# Create an h-function for a goal state in MAPPGridState
# The h-estimate is the maximum of the Manhattan distances
# to goal positions for each agent.
class MAPPDistanceMax(MAPPHeuristic):
    """Use the max individual agent distance to goal as heuristic."""
    def __init__(self,goal):
        super().__init__(goal)

    def __call__(self,state):
        """ 
        See MAPPHeuristic.__call__ 
        """
        return max(manhattan(u,v) for (u,v) in zip(self.goal.agents,
                                                   state.agents))

# A more informative heuristic is the sum of the Manhattan distances.
class MAPPDistanceSum(MAPPHeuristic):
    """Use the sum of distance to goal for all agents as heuristic."""
    
    def __init__(self,goal):
        super().__init__(goal)
        
    def __call__(self,state):
        """ 
        See MAPPHeuristic.__call__ 
        """
        return sum(manhattan(u,v) for (u,v) in zip(self.goal.agents,
                                                   state.agents))

def manhattan(u,v):
    """ 
    Manhattan distance between two points. 
    
    Helper function.
    
    Parameters
    ----------
    u : pair of (int,int)
    v : pair of (int,int)

    Returns
    -------
    int
       Manhattan distance.
    """
    x1,y1 = u
    x2,y2 = v
    return abs(x1-x2) + abs(y1-y2)


if __name__ == "__main__":
    # Some examples:
    grid_S = MAPPGridState([(0,0),(1,1),(0,1),(1,0)],nrows=5,ncols=5,walls=[])
    grid_G = MAPPGridState([(0,0),(4,4),(0,4),(4,0)],nrows=5,ncols=5,walls=[])
    h_max = MAPPDistanceMax(grid_G)
    h_sum = MAPPDistanceSum(grid_G)
    print("Distance heuristics from state")
    print(grid_S)
    print("to state")
    print(grid_G)
    printf("is h_max = {h_max(grid_S)}, h_sum = {h_sum(grid_S)}.")

    grid_T = MAPPGridState([(0,0),(3,3),(0,1),(1,0)],nrows=5,ncols=5,walls=[])
    print("Distance heuristics from state")
    print(grid_T)
    print("to state")
    print(grid_G)
    printf("is h_max = {h_max(grid_T)}, h_sum = {h_sum(grid_T)}.")

