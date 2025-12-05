import functions

manifestName = input("Enter the manifest: ")
containers = []

# read file
with open(manifestName, "r") as text:
    for line in text:
        # split each row by the commas
        parts = [p.strip() for p in line.split(", ")]

        # first part will be the location - tuple (x,y)
        part1 = parts[0][1:-1]

        x, y = part1.split(",")
        location = (int(x),int(y))

        # second part is weight - int
        weight = parts[1][1:-1]
        weight = int(weight)

        # third part is contents - str
        contents = parts[2]
        container = functions.Container(location, weight, contents)
        containers.append(container)

#creating start state
grid = functions.shipGrid(containers)
left = functions.left(grid)
right = functions.right(grid)
goal = functions.reachGoal(grid)
initialState = functions.state(grid, left, right, goal, 0, parent=None)

#see if it is an edge case, else run BFS and Astar
foundGoal = initialState
isEdge = functions.edgeCase(initialState , containers)
if not isEdge:

    #run all 3 algorithms 
    BFSGoal = functions.BFS(initialState)
    BFStime = functions.totalTime(BFSGoal)
    print(f"\nBFS total time was {BFStime} minutes\n")
    AStarGoal = functions.AStar(initialState)
    AStartime = functions.totalTime(AStarGoal)
    print(f"\nAStar total time was {AStartime} minutes\n")
    AStar2Goal = functions.AStar2(initialState)
    AStar2Time = functions.totalTime(AStar2Goal)
    print(f"\nAStar2 total time was {AStar2Time} minutes\n")
    AStar3Goal = functions.AStar3(initialState)
    AStar3Time = functions.totalTime(AStar3Goal)
    print(f"\nAStar3 total time was {AStar3Time} minutes\n")

    results = [
    ("BFS", BFSGoal, BFStime),
    ("AStar", AStarGoal, AStartime),
    ("AStar2", AStar2Goal, AStar2Time),
    ("AStar3", AStar3Goal, AStar3Time)
    ]

    bestName, bestGoal, bestTime = min(results, key=lambda x: x[2])

    print(f"\nBest Algorithm: {bestName} with {bestTime} minutes, manifest updated with this algorithm\n")    
    functions.updateManifest(bestGoal.grid, manifestName)
else:
    print("\n This case was one of the edge cases, no need for BFS/Astar. Manifest is same.\n")


