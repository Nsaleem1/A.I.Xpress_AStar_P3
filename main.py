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
    foundGoal = functions.BFS(initialState)
    print(f"\nBFS total time was {foundGoal.time} minutes\n")
    foundGoal = functions.AStar(initialState)
    functions.backtrack(foundGoal, initialState)
    print(f"\nAstar total time was {foundGoal.time} minutes\n")
    print("Updated Manifest is for Astar and the Moves.txt file\n")
    functions.updateManifest(foundGoal.grid, manifestName)
else:
    print("\n This case was one of the edge cases, no need for BFS/Astar. Manifest is same.\n")


