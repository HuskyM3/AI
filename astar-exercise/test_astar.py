""" Tests for astar search."""

import unittest
import itertools
from astar import astar
from action import Action
from state import State
from mappstate import MAPPState
from mappdistance import MAPPDistanceSum

class TestAstar(unittest.TestCase):
    """Tests for astar search method."""

    def setUp(self):
        self.mapp_1_s = MAPPState.create_from_string(["1..",
                                                          "...",
                                                          "..."])
        self.mapp_1_g = MAPPState.create_from_string(["...",
                                                          "...",
                                                          "..1"])
    def test_0_return(self):
        """A correct call (a plan exists) to astar should not return None."""
        plan = astar(MAPPDistanceSum(self.mapp_1_g),
                     self.mapp_1_s,
                     lambda s : s == self.mapp_1_g)
        self.assertIsNotNone(plan, "Have you forgotten the return statement?")

    def test_1_return(self):
        """Function astar should return a iterable (list) of actions."""
        plan = list(astar(MAPPDistanceSum(self.mapp_1_g),
                          self.mapp_1_s,
                          lambda s : s == self.mapp_1_g))
        for a in plan:
            self.assertIsInstance(a,Action)

    def test_2_return(self):
        """If start_state satisfies goaltest the plan should be empty list."""
        plan = list(astar(MAPPDistanceSum(self.mapp_1_s),
                          self.mapp_1_s,
                          lambda s : s == self.mapp_1_s))
        self.assertEqual(len(plan),0)

    def test_3_basic(self):
        """Moving a single agent diagonally (0,0)->(3,3) should take four actions."""
        plan = list(astar(MAPPDistanceSum(self.mapp_1_g),
                          self.mapp_1_s,
                          lambda s : s == self.mapp_1_g))
        self.assertEqual(4,len(plan))
        
    def test_4_open(self):
        """Solving this 5x5 MAPP should have a cost of 16."""
        grid_S = MAPPState([(0,0),(1,1),(0,1),(1,0)],nrows=5,ncols=5,walls=[])
        grid_G = MAPPState([(3,3),(2,2),(2,3),(3,2)],nrows=5,ncols=5,walls=[])
        plan = astar(MAPPDistanceSum(grid_G),
                     grid_S,
                     lambda s : s == grid_G)
        self.assertEqual(16,sum(a.cost for a in plan))
        
    def test_5_correctness(self):
        """The best solution (least cost) should be returned, not the first one."""
        # TermTestState (see below) is designed so that the first solution found
        # has a higher cost than the second solution.
        # Start in stateindex 1 and look for path to index 0.
        plan = list(astar(TermTestState.TermTestH, # function: distance to goal
                          TermTestState(),
                          lambda state: (state.state == 0))) # goal test

        correct = [Action("1", "3", cost=1.0),
                   Action("3", "4", cost=0.5),
                   Action("4", "5", cost=0.5),
                   Action("5", "6", cost=0.5),
                   Action("6", "G", cost=0.5)]
        
        cost = sum(p.cost for p in plan)
        c_cost = sum(c.cost for c in correct)
        # Check cost
        self.assertEqual(cost, c_cost,
                         f"Correct cost {c_cost}, your plan cost: {cost}. Check so you return the best solution, and not only the first one found if you have too high cost. Check so you return the full path if too low."
        )
        # Check path in general.
        self.assertTrue(len(plan) == len(correct) and all(p == c for p,c in zip(plan,correct)),
                        f"Correct plan: {correct}; Your plan: {plan}; Make sure that the plan isn't e.g. reversed.")

    def test_6_walls(self):
        """Solving this 5 x 7 MAPP should have a cost of 10."""
        grid_S = MAPPState.create_from_string(
            ["#.#0###",
             "#.#.###",
             ".......",
             "###.#.#",
             "###.#1#"])
        
        grid_G = MAPPState.create_from_string(
            ["#.#1###",
             "#.#.###",
             ".......",
             "###.#.#",
             "###0#.#"])
        plan = astar(MAPPDistanceSum(grid_G),
                     grid_S,
                     lambda s : s == grid_G)
        self.assertEqual(10,sum(a.cost for a in plan))
 
 
    def test_7_medium(self):
        """Solving this 9x13 MAPP should have a cost of 36."""
        grid_S = MAPPState.create_from_string(
            ["...#.........",
             "...#.........",
             "...#.........",
             "...########..",
             "..12......34.",
             "...###..###..",
             "...######....",
             "........#....",
             "........#...."])
        
        grid_G = MAPPState.create_from_string(
            ["...#.........",
             "...#.........",
             "...#.........",
             "...########..",
             "..34......21.",
             "...###..###..",
             "...######....",
             "........#....",
             "........#...."])
        plan = astar(MAPPDistanceSum(grid_G),
                     grid_S,
                     lambda s : s == grid_G)
        self.assertEqual(36,sum(a.cost for a in plan))
 

                         


class TermTestState(State):
    """
    State class designed to provide a higher cost path to goal first.
    """
    def __init__(self,stateindex = 1):
        self.state = stateindex

    # Construct a string representing a state.
    def __repr__(self):
        return str(self.state)
    # The hash function for states, mapping each state to an integer
    def __hash__(self):
        return self.state

    # Equality of states.
    def __eq__(self,other):
        return (self.state == other.state)

    # queue.PriorityQueue needs an ordering of states
    def __lt__(self,other):
        return False

    # Compute all successors
    # 1 has 2, 3
    # 2 has 0 (the goal state)
    # 3 has 4
    # 4 has 5
    # 5 has 6
    # 6 has 0
    def successors(self):
        if self.state == 1:
            return [ (Action("1","2",1.0),TermTestState(2)),
                     (Action("1","3",1.0),TermTestState(3)) ]
        elif self.state == 2:
            return [ (Action("2","G",5.0),TermTestState(0)) ]
        elif self.state == 3:
            return [ (Action("3","4",0.5),TermTestState(4)) ]
        elif self.state == 4:
            return [ (Action("4","5",0.5),TermTestState(5)) ]
        elif self.state == 5:
            return [ (Action("5","6",0.5),TermTestState(6)) ]
        elif self.state == 6:
            return [ (Action("6","G",0.5),TermTestState(0)) ]
        elif self.state == 0:
            return [ ]
        else:
            return 0.0

    # Create an h-function so that the path to 0 through 2
    # is found first, and the optimal path (which is longer)
    # is found later.
    # Static method in class.
    def TermTestH(s):
        if s.state == 0:
            return 0.0
        elif s.state == 1:
            return 2.0
        elif s.state == 2:
            return 1.0
        elif s.state == 3:
            return 2.0
        elif s.state == 4:
            return 1.5
        elif s.state == 5:
            return 1.0
        elif s.state == 6:
            return 0.5
        else:
            return 0.0

if __name__ == "__main__":
    unittest.main()
