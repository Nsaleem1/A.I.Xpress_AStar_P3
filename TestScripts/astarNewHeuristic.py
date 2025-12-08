import copy
import heapq
from itertools import count
import functions
import time

class Container:
    def __init__(self, location, weight, contents):
        self.location = location
        self.weight = weight
        self.contents = contents

class State:
    def __init__(self, grid, left, right, goal, time, parent):
        self.grid = grid
        self.left = left
        self.right = right
        self.goal = goal
        self.time = time
        self.parent = parent

    def __eq__(self, other):
        return isinstance(other, State) and self.grid == other.grid

def read_manifest(filename):
    containers = []
    with open(filename, "r") as f:
        for line in f:
            parts = [p.strip() for p in line.split(", ")]
            x, y = map(int, parts[0][1:-1].split(","))
            weight = int(parts[1][1:-1])
            contents = parts[2]
            containers.append(Container((x, y), weight, contents))
    return containers

# List of test files
test_files = ["ShipCase1.txt", "ShipCase2.txt", "ShipCase3.txt", "ShipCase4.txt", "ShipCase5.txt", "ShipCase6.txt"]

def newHeuristic(state):
    grid = state.grid
    leftW = functions.left(grid)
    rightW = functions.right(grid)

    misplaced = 0

    if leftW > rightW:
        for r in range(1, 9):
            for c in range(1, 13 // 2 + 1):
                if grid[r][c][1] not in ("UNUSED", "NAN"):
                    misplaced += 1

    elif rightW > leftW:
        for r in range(1, 9):
            for c in range(13 // 2 + 1, 13):
                if grid[r][c][1] not in ("UNUSED", "NAN"):
                    misplaced += 1
    return state.time + misplaced

def AStarNew(start, heuristic):
    counter = count()
    unvisited = []
    minWeight = float('inf')
    heapq.heappush(unvisited, (heuristic(start), next(counter), start))
    grid_to_tuple = lambda g: tuple(tuple(row) for row in g)
    cost_so_far = {grid_to_tuple(start.grid): start.time}

    iterations = 0
    max_iterations = 100000  # safety cap

    while unvisited and iterations < max_iterations:
        _, _, currState = heapq.heappop(unvisited)
        #Goal check
        if functions.reachGoal(currState.grid):
            return currState
        # Generate neighbors
        nextMoves = functions.computeMoves(currState)

        for neighbor in nextMoves:
            neighbor_tuple = grid_to_tuple(neighbor.grid)
            newCost = neighbor.time
            if neighbor_tuple not in cost_so_far or newCost < cost_so_far[neighbor_tuple]:
                cost_so_far[neighbor_tuple] = newCost
                neighbor.parent = currState
                fValue = newCost + heuristic(neighbor)
                heapq.heappush(unvisited, (fValue, next(counter), neighbor))

        weightVal = abs(functions.left(currState.grid) - functions.right(currState.grid))
        if weightVal < minWeight:
            minWeight = weightVal
            minState = currState

        iterations += 1

    return minState


def totalTime(goalState):
    if goalState.parent is None:
        return goalState.time
    try:
        second, beforeLast, start = functions.secondStates(goalState)
        craneGrid, _, _ = functions.craneToGrid(start.grid, second.grid)
        gridCrane, _, _ = functions.gridToCrane(beforeLast.grid, goalState.grid)
        total = goalState.time + craneGrid + gridCrane
        return total
    except AttributeError:
        return goalState.time

for test_file in test_files:
    containers = read_manifest(test_file)

    grid = functions.shipGrid(containers)
    start_state = State(
        grid,
        functions.left(grid),
        functions.right(grid),
        functions.reachGoal(grid),
        0,
        None
    )
    start_time = time.time()
    goal_state = AStarNew(start_state, newHeuristic)
    runtime = time.time() - start_time
    print(f"Runtime for {test_file}: {runtime:.4f} seconds")

    print(f"Total time for {test_file}: {totalTime(goal_state)} minutes")