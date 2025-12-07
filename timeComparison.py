import time
import functions
import os
import matplotlib.pyplot as plt
import moveCount

def readFile(manifestName):
    containers = []
    # read file
    with open(manifestName, "r") as text:
        for line in text:
            parts = [p.strip() for p in line.split(", ")]

            part1 = parts[0][1:-1]

            x, y = part1.split(",")
            location = (int(x),int(y))

            weight = parts[1][1:-1]
            weight = int(weight)

            contents = parts[2]
            container = functions.Container(location, weight, contents)
            containers.append(container)

    grid = functions.shipGrid(containers)
    left = functions.left(grid)
    right = functions.right(grid)
    goal = functions.reachGoal(grid)
    initialState = functions.state(grid, left, right, goal, 0, parent=None)
    
    return initialState

def run_algorithm(manifestName):
    initialState = readFile(manifestName)
    results = {}
    start_comp = time.time()
    goal = functions.BFS(initialState)
    end_comp = time.time()

    computation_time = end_comp - start_comp

    # If algorithm fails, return "infinite" solution time
    if goal is None:
        return float('inf'), computation_time

    solution_time = functions.totalTime(goal)
    return solution_time, computation_time


# ----------------------------------------
# LOOP THROUGH ALL TEST FILES
# ----------------------------------------

test_files = [
    "ShipCase1.txt",
    "ShipCase2.txt",
    "ShipCase3.txt",
    "ShipCase4.txt",
    "ShipCase5.txt",
    "ShipCase6.txt"
]

BFS_solution = []
A_solution = []

BFS_compute = []
A_compute = []

for filename in test_files:
    print(f"\nRunning on {filename}...")
    initialState = readFile(filename)

    sol_BFS, comp_BFS = run_algorithm(functions.BFS, initialState)
    sol_A, comp_A = run_algorithm(functions.AStar, initialState)

    BFS_solution.append(sol_BFS)
    BFS_compute.append(comp_BFS)

    A_solution.append(sol_A)
    A_compute.append(comp_A)

# ----------------------------------------
# COMBINED BAR CHARTS
# ----------------------------------------

x = range(len(test_files))

# solution time
plt.figure(figsize=(10, 5))
plt.bar([i - 0.2 for i in x], BFS_solution, width=0.4, label="BFS")
plt.bar([i + 0.2 for i in x], A_solution, width=0.4, label="A*")
plt.title("Solution Time Across Test Cases")
plt.xlabel("Test Case")
plt.ylabel("Solution Time (minutes)")
plt.xticks(x, test_files)
plt.legend()
plt.tight_layout()
plt.show()

# computation time
plt.figure(figsize=(10, 5))
plt.bar([i - 0.2 for i in x], BFS_compute, width=0.4, label="BFS")
plt.bar([i + 0.2 for i in x], A_compute, width=0.4, label="A*")
plt.title("Computation Time Across Test Cases")
plt.xlabel("Test Case")
plt.ylabel("Computation Time (seconds)")
plt.xticks(x, test_files)
plt.legend()
plt.tight_layout()
plt.show()
