import functions
import time 

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

    # BFS
    start = time.time()
    BFSGoal = functions.BFS(initialState)
    end = time.time()
    BFS_compute = end - start  
    BFS_solution = functions.totalTime(BFSGoal)  

    print("\n----- BFS Results -----")
    print(f"BFS compute time: {BFS_compute:.5f} seconds")
    print(f"BFS solution time: {BFS_solution} minutes\n")

    # A*
    start = time.time()
    AStar3Goal = functions.AStar3(initialState)
    end = time.time()
    AStar3_compute = end - start
    AStar3_solution = functions.totalTime(AStar3Goal)

    print("----- AStar3 Results -----")
    print(f"AStar3 compute time: {AStar3_compute:.5f} seconds")
    print(f"AStar3 solution time: {AStar3_solution} minutes\n")

else:
    print("\n This case was one of the edge cases, no need for BFS/Astar. Manifest is same.\n")


