
from idastar import IDAstar
from stacks import StackState, stackDistance

if __name__ == "__main__":
    # A few basic examples/tests.
    from mappgridstate import MAPPGridState
    from mappdistance import MAPPDistanceSum
    import time

    EXAMPLES = [("Example 0",
                 MAPPGridState.create_from_string(
                    ["123.",
                     "....",
                     "....",
                     "...."]),
                 MAPPGridState.create_from_string(
                    ["....",
                     ".12.",
                     "..3.",
                     "...."]),
                 MAPPDistanceSum,
                 "6.0",
                 "< 1 second"),
                ("Example 1a",
                 StackState.makeFromStrings(["321","4",""]),
                 StackState.makeFromStrings(["1234","",""]),
                 stackDistance,
                 "8",
                 "< 1 seconds"),
                ("Example 1b",
                 StackState.makeFromStrings(["321","456","",""]),
                 StackState.makeFromStrings(["","","615234",""]),
                 stackDistance,
                 "6",
                 "< 1 second"),
                ("Example 1c",
                 StackState.makeFromStrings(["321","456","7","","",""]),
                 StackState.makeFromStrings(["","","","6152347","",""]),
                 stackDistance,
                 "7",
                 "< 1 second"),
                ("Example 1d",
                 StackState.makeFromStrings(["8321","9456","A7","","",""]),
                 StackState.makeFromStrings(["","89A","","6152347","",""]),
                 stackDistance,
                 "11",
                 "< 1 second"),
                ("Example 1e",
                 StackState.makeFromStrings(["8321","945","A76","","",""]),
                 StackState.makeFromStrings(["89A","6152347","","","",""]),
                 stackDistance,
                 "12",
                 "< 1 second"),
                ("Example 1f",
                 StackState.makeFromStrings(["8321","945","A76",""]),
                 StackState.makeFromStrings(["89A","1652347","",""]),
                 stackDistance,
                 "13",
                 "< 1 second"),
                ("Example 1g",
                 StackState.makeFromStrings(["8321","945","AB76",""]),
                 StackState.makeFromStrings(["89AB","1652347","",""]),
                 stackDistance,
                 "15",
                 "< 1 second"),
                ("Example 1h",
                 StackState.makeFromStrings(["8321","945","AB76C","",""]),
                 StackState.makeFromStrings(["89AB","1C652347","","",""]),
                 stackDistance,
                 "15",
                 "< 5 seconds"),
                ("Example 1i",
                 StackState.makeFromStrings(["123","456","789"]),
                 StackState.makeFromStrings(["147","258","369"]),
                 stackDistance,
                 "17",
                 "< 20 seconds"),
                ("Example 1j",
                 StackState.makeFromStrings(["8321","945","AB76C","","",""]),
                 StackState.makeFromStrings(["89AB","1C652347","","","",""]),
                 stackDistance,
                 "15",
                 "< 30 seconds"),
                ("Example 1k",
                 StackState.makeFromStrings(["8321","945","AB76CDE",""]),
                 StackState.makeFromStrings(["89AB","D1C6E52347","",""]),
                 stackDistance,
                 "19",
                 "< 60 seconds"),
                ("Example 1l",
                 StackState.makeFromStrings(["8321","945","AB76CDE","",""]),
                 StackState.makeFromStrings(["89AB","D1C6E52347","","",""]),
                 stackDistance,
                 "18",
                 "< 2 minutes"),
                ("Example 1m",
                 StackState.makeFromStrings(["8321","945","AB76CDE","F","",""]),
                 StackState.makeFromStrings(["F89AB","","","","D1C6E52347",""]),
                 stackDistance,
                 "18",
                 "< 30 seconds"),
                ("Example 2",
                 MAPPGridState([(0,0),(1,1),(0,1),(1,0)],nrows=5,ncols=5,walls=[]),
                 MAPPGridState([(3,3),(2,2),(2,3),(3,2)],nrows=5,ncols=5,walls=[]),
                 MAPPDistanceSum,
                 "16.0",
                 "< 10 seconds"),
                ("Example 3a",
                 MAPPGridState.create_from_string(
                    ["..#..",
                     ".1#..",
                     "..#..",
                     ".....",
                     "..#..",
                     "..#..",
                     "..#.."]),
                 MAPPGridState.create_from_string(
                    ["..#..",
                     "..#..",
                     "..#..",
                     ".....",
                     "..#..",
                     "..#1.",
                     "..#.."]),
                 MAPPDistanceSum,
                 "6.0",
                 "< 10 minutes"),
                ("Example 3b",
                 MAPPGridState.create_from_string(
                    ["..#..",
                     ".1#..",
                     ".2#..",
                     ".....",
                     "..#3.",
                     "..#..",
                     "..#.."]),
                 MAPPGridState.create_from_string(
                    ["..#..",
                     "..#..",
                     ".3#..",
                     ".....",
                     "..#2.",
                     "..#1.",
                     "..#.."]),
                 MAPPDistanceSum,
                 "18.0",
                 "< 2 seconds"),
                ("Example 3c",
                 MAPPGridState.create_from_string(
                    ["..#..",
                     ".1#..",
                     ".2#..",
                     ".....",
                     "..#3.",
                     "..#4.",
                     "..#.."]),
                 MAPPGridState.create_from_string(
                    ["..#..",
                     ".4#..",
                     ".3#..",
                     ".....",
                     "..#2.",
                     "..#1.",
                     "..#.."]),
                 MAPPDistanceSum,
                 "26.0",
                 "< 5 minutes"),
                ("Example 4a",
                 MAPPGridState.create_from_string(
                    [".#........",
                     ".########.",
                     ".01.....2.",
                     ".###..###.",
                     ".######...",
                     "......#..."]),
                 MAPPGridState.create_from_string(
                     [".#........",
                      ".########.",
                      ".2.....10.",
                      ".###..###.",
                      ".######...",
                      "......#..."]),
                 MAPPDistanceSum,
                 "23.0",
                 "< 1 second"),
                ("Example 4b",
                 MAPPGridState.create_from_string(
                    [".#........",
                     ".########.",
                     ".01....32.",
                     ".###..###.",
                     ".######...",
                     "......#..."]),
                 MAPPGridState.create_from_string(
                     [".#........",
                      ".########.",
                      ".23....10.",
                      ".###..###.",
                      ".######...",
                      "......#..."]),
                 MAPPDistanceSum,
                 "30.0",
                 "< 5 seconds")#,
#                ("Example 5a",
#                 MAPPGridState.create_from_string(
#                    [".......",
#                     ".......",
#                     ".123...",
#                     ".45....",
#                     ".......",
#                     "......."]),
#                 MAPPGridState.create_from_string(
#                     ["......",
#                      "......",
#                      "......",
#                      "..123.",
#                      "...45.",
#                      "......"]),
#                 MAPPDistanceSum,
#                 "12.0",
#                 "5 minutes"),
#                ("Example 5b",
#                 MAPPGridState.create_from_string(
#                    ["........",
#                     "........",
#                     ".123....",
#                     ".456....",
#                     "........",
#                     "........"]),
#                 MAPPGridState.create_from_string(
#                     [".......",
#                      ".......",
#                      ".......",
#                      "..123..",
#                      "...456.",
#                      "......."]),
#                 MAPPDistanceSum,
#                 "15.0",
#                 "5 minutes")
                ]

    for (name,S,G,D,C,T) in EXAMPLES:
        print("=========== Problem instance: " + name + " ==============")
        print("A* runtime estimate: " + T)
        for pname,planner in [("IDA*",IDAstar)
                              ]:
            print("---------------------------------------")
            print("Running " + name + " with " + pname)
            stime = time.process_time()
            result = planner(S,
                             lambda state: state == G, 
                             D(G))
            etime = time.process_time()
            if result == None:
                print("No plan")
            else:
                plan = list(result)
                print(f"Plan:")
                s = S
                print(s)
                for i,p in enumerate(plan):
                    s = s.apply(p)
                    print(f"step: {i}, cost: {p.cost}")
                    print(str(s))
                print(f"{pname} runtime for {name}: {etime-stime}")
                print(f"Cost of solution: {sum(p.cost for p in plan)}")
                print("Optimal cost: " + C)
