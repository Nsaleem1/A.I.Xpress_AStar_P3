import time
import functions
import os
import matplotlib.pyplot as plt

os.makedirs("outbound", exist_ok=True)

def save_outbound_manifest(goalState, case_number):
    os.makedirs("outbound", exist_ok=True)
    filename = f"AutoTest{case_number:02d}OUTBOUND.txt"
    filepath = os.path.join("outbound", filename)
    grid = goalState.grid

    with open(filepath, "w") as f:
        for r in range(1, 9):
            for c in range(1, 13):
                weight, content = grid[r][c]
                row = f"{r:02d}"
                col = f"{c:02d}"
                f.write(f"[{row},{col}], {{{weight:05d}}}, {content}\n")

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

def runtimeTest(manifestName):
    initialState = readFile(manifestName)
    results = {}

   # --------------- BFS -----------------
    start_time = time.time()
    bfs_goal = functions.BFS(initialState)
    bfs_runtime = time.time() - start_time

    if bfs_goal is None or bfs_goal.parent is None:
        results["BFS"] = (bfs_runtime, None, None)
        print(f"BFS Runtime: 0 seconds")
        print(f"BFS Solution time: 0 minutes")
    else:
        bfs_solution_time = functions.totalTime(bfs_goal)

        print(f"BFS runtime: {bfs_runtime:.4f} seconds")
        print(f"BFS Solution time: {bfs_solution_time} minutes")

        results["BFS"] = (bfs_runtime, bfs_solution_time)
      
    # ------------------ A* ------------------
    start_time = time.time()
    astar_goal = functions.AStar(initialState)
    astar_runtime = time.time() - start_time

    if astar_goal is None or astar_goal.parent is None:
        results["AStar"] = (astar_runtime, None, None)
        print(f"A* Runtime: {astar_runtime:.4f} seconds")
        print(f"A* Solution time: 0 minutes")
        case_number = int(file.split("_")[1].split(".")[0])  

        save_outbound_manifest(astar_goal, case_number)
    else:
        astar_solution_time = functions.totalTime(astar_goal)

        print(f"A* Runtime: {astar_runtime:.4f} seconds")
        print(f"A* Solution time: {astar_solution_time} minutes")
        case_number = int(file.split("_")[1].split(".")[0])  

        save_outbound_manifest(astar_goal, case_number)
        results["AStar"] = (astar_runtime, astar_solution_time)

    return results

#Original test cases
test_files = [
    "ShipCase1.txt",
    "ShipCase2.txt",
    "ShipCase3.txt",
    "ShipCase4.txt",
    "ShipCase5.txt",
    "ShipCase6.txt"
]

"""# 20 manifest tests
test_directory = "Additional Tests"
test_files = []
for f in os.listdir(test_directory):
    if f.endswith(".txt"):
        test_files.append(os.path.join(test_directory, f))

test_files.sort()"""

all_results = {}


for file in test_files:
    try:
        print(f"Test file: {file}")
        all_results[file] = runtimeTest(file)
    except FileNotFoundError:
        print(f"Skipping {file}: file not found.")

tests = list(all_results.keys())
bfs_runtimes = [all_results[t]["BFS"][0] for t in tests]
astar_runtimes = [all_results[t]["AStar"][0] for t in tests]

bfs_sol = [all_results[t]["BFS"][1] for t in tests]
astar_sol = [all_results[t]["AStar"][1] for t in tests]

# ----------------- Runtime Plot ---------------------
import numpy as np

bfs_sol = [v if v is not None else 0 for v in bfs_sol]
astar_sol = [v if v is not None else 0 for v in astar_sol]

x = np.arange(len(test_files))        
width = 0.35                         

plt.figure(figsize=(12, 6))

plt.bar(x - width/2, bfs_runtimes, width, label="BFS")
plt.bar(x + width/2, astar_runtimes, width, label="A*")

plt.yscale("log")

plt.xlabel("Test Case")
plt.ylabel("Runtime (seconds, log scale)")
plt.title("Runtime Comparison: BFS vs A*")
plt.xticks(x, [str(i+1) for i in range(len(test_files))])
plt.legend()

for i, v in enumerate(bfs_runtimes):
    plt.text(i - width/2, v, f"{v:.4f}", fontsize=7, ha='center', va='bottom')

for i, v in enumerate(astar_runtimes):
    plt.text(i + width/2, v, f"{v:.4f}", fontsize=7, ha='center', va='bottom')

plt.tight_layout()
plt.show()


# ----------------- Solution Time Plot ---------------------

plt.figure(figsize=(12, 6))

plt.bar(x - width/2, bfs_sol, width, label="BFS")
plt.bar(x + width/2, astar_sol, width, label="A*")

plt.xlabel("Test Case")
plt.ylabel("Solution Time (minutes)")
plt.title("Solution Time Comparison: BFS vs A*")
plt.xticks(x, [str(i+1) for i in range(len(test_files))])
plt.legend()

for i, v in enumerate(bfs_sol):
    if v is not None:
        plt.text(i - width/2, v, f"{v:.1f}", fontsize=7, ha='center', va='bottom')

for i, v in enumerate(astar_sol):
    if v is not None:
        plt.text(i + width/2, v, f"{v:.1f}", fontsize=7, ha='center', va='bottom')

plt.tight_layout()
plt.show()
