import math
import matplotlib.pyplot as plt
import random
import copy
from collections import deque
import os

import heapq
from itertools import count
class state:
    def __init__(self, grid, left, right, goal, time, parent):
        self.grid = grid
        self.left = left
        self.right = right
        self.goal = goal 
        self.time = time 
        self.parent = parent

    def __eq__(self, other):
        return isinstance(other, state) and self.grid == other.grid


#ship grid, contains the grid with a grid object
# grid object has weight,content 
def shipGrid(containers):
    #create a matrix 9 x 13 (one more since manifest not start at (0,0))
    grid = [[(0,"NAN") for _ in range(13)] for _ in range(9)]
    #grid = [[(0,"UNUSED") for _ in range(13)] for _ in range(9)]

    for container in containers:
        row,col = container.location
        grid[row][col] = (int(container.weight), str(container.contents))
    return grid

def left(grid):
    totalWeight = 0
    for i in range(1,9):
        for j in range(1, 13 // 2 + 1):
            if (grid[i][j][1] != "NAN"):
                totalWeight += grid[i][j][0]
    return totalWeight

def right(grid):
    totalWeight = 0
    for i in range(1,9):
        for j in range(13 // 2 + 1, 13):
            if grid[i][j][1] != "NAN":
                totalWeight += grid[i][j][0]
    return totalWeight

def reachGoal(grid):
    leftVal = left(grid)
    rightVal = right(grid)
    if abs(leftVal - rightVal) < (sum([leftVal, rightVal]) * 0.10):
        return True
    return False


# def newState(oldRow, oldCol, newRow, newCol, currState):
#     grid = currState.grid
#     value = grid[oldRow][oldCol][0]
#     content = grid[oldRow][oldCol][1]

#     #empty curr location
#     grid[oldRow][oldCol] = (0, "UNUSED")
#     #add to new loc
#     grid[newRow][newCol] = (value, content)

#     time = manhattan((oldRow, oldCol), (newRow, newCol)) + currState.time

#     return state(grid, left(grid), right(grid), reachGoal(grid), time)
def newState(oldRow, oldCol, newRow, newCol, currState):
    grid = copy.deepcopy(currState.grid)   # ← FIXED

    value, content = grid[oldRow][oldCol]

    grid[oldRow][oldCol] = (0, "UNUSED")
    grid[newRow][newCol] = (value, content)

    time = manhattan((oldRow, oldCol), (newRow, newCol)) + currState.time

    return state(grid, left(grid), right(grid), reachGoal(grid), time, currState)

# assume that 0 means spot is empty
# None is spot we cant go to 
# make sure not to put anything in the 0 row/column
def computeMoves(state):
    grid = state.grid
    nextStates = []
    checkedCol = []

    #look at top of each column
    # compute all moves for that container
  
    for i in range (1,9):
        for j in range(1,13):

            checkedCol = []
            #so we dont check like the spot above us to move to since we cant move there
            checkedCol.append(j)

            # this container is on the top since above it is 0, and container itself cant be 0 or NAN
            # need two cases bc if I m at like row 8 then above is out of the grid

            if (i == 8 and grid[i][j][0] != 0 and grid[i][j][1] != "NAN"):    
                # find an empty spot
                for row in range (1,9):
                    for col in range (1,13):
                        if (grid[row][col][0] == 0 and grid[row][col][1] != "NAN" and not (col in checkedCol)):
                            nextStates.append(newState(i, j, row, col, copy.deepcopy(state)))
                            checkedCol.append(col)
            
            elif ((i < 8) and (grid[i+1][j][0] == 0) and (grid[i][j][0] != 0) and (grid[i][j][1] != "NAN")):
                for row in range (1,9):
                    for col in range (1,13):
                        if (grid[row][col][0] == 0 and grid[row][col][1] != "NAN" and not (col in checkedCol)):
                            nextStates.append(newState(i, j, row, col, copy.deepcopy(state)))
                            checkedCol.append(col)

    return nextStates

def edgeCase(initialState, containers):
    count = 0
    rightCnt = 0
    leftCnt = 0

    #empty grid
    if (left(initialState.grid) == 0 and right(initialState.grid) == 0):
        return True
    
    #already balanced
    if (reachGoal(initialState.grid)):
        return True

    #one container on right
    if (left(initialState.grid) == 0):
        for container in containers[48:97]:
            if (container.weight != 0):
                count += 1
        if count == 1:
            return True
        
    count = 0

     #one container on left
    if (left(initialState.grid) == 0):
        for container in containers[0:48]:
            if (container.weight != 0):
                count += 1
        if count == 1:
            return True

    #two containers on opp sides
    for container in containers[0:48]:
        if (container.weight != 0):
            leftCnt += 1
    for container in containers[48:97]:
        if (container.weight != 0):
            rightCnt += 1 
    if (leftCnt == rightCnt and leftCnt == 1):
        return True     

    return False   

def BFS(start):

    minWeight = float('inf')
    unvisited = deque([start])
    visited = set()

    #this is to get the grid as coordinates (x,y) so we can compare grids
    grid_to_tuple = lambda grid: tuple(tuple(row) for row in grid)

    visited.add(grid_to_tuple(start.grid))
    while unvisited:
        #select state from queue, get its next states
        currState = unvisited.popleft()
        nextMoves = computeMoves(copy.deepcopy(currState))

        #calculate next states
        for neighbor in nextMoves:
            #convert the grid to tuple
            neighbor_grid_tuple = grid_to_tuple(neighbor.grid)
            if neighbor_grid_tuple not in visited:
                neighbor.parent = currState
                unvisited.append(neighbor)
                visited.add(neighbor_grid_tuple)


        #if its goal, we are done
        if reachGoal(currState.grid):
            return currState

        #keep track of most balanced option too 
        weightVal = abs(left(currState.grid) - right(currState.grid))
        if weightVal < minWeight:
            minWeight = weightVal
            minState = currState
     
    return minState

# my heuristic is time + total distance 
# choosing the move with less time and makes more balanced 
def Astar(start):

    #need this counter to break ties for heuristic
    counter = count()
    minWeight = float('inf')
    unvisited = []
    heapq.heappush(unvisited, (0, next(counter), start))
    visited = set()
   
    #this is to get the grid as coordinates (x,y) so we can compare grids
    grid_to_tuple = lambda grid: tuple(tuple(row) for row in grid)

    visited.add(grid_to_tuple(start.grid))
    while unvisited:
        #select state from queue, get its next states
        priority, _, currState = heapq.heappop(unvisited)
        nextMoves = computeMoves(copy.deepcopy(currState))

        # calculate next states
        for neighbor in nextMoves:
            #convert the grid to tuple
            neighbor_grid_tuple = grid_to_tuple(neighbor.grid)
            if neighbor_grid_tuple not in visited:
                neighbor.parent = currState
                heapq.heappush(unvisited, (computeHeuristic(neighbor), next(counter), neighbor))
                visited.add(neighbor_grid_tuple)

        #if its goal, we are done
        if reachGoal(currState.grid):
            return currState
             
        #keep track of most balanced option too 
        weightVal = abs(left(currState.grid) - right(currState.grid))
        if weightVal < minWeight:
            minWeight = weightVal
            minState = currState
     
    return minState

def AStarOptimal(start):
    counter = count()
    unvisited = []
    heapq.heappush(unvisited, (computeHeuristic(start), next(counter), start))

    grid_to_tuple = lambda g: tuple(tuple(row) for row in g)
    cost_so_far = {grid_to_tuple(start.grid): start.time}

    minWeight = abs(left(start.grid) - right(start.grid))
    minState = start

    while unvisited:
        _, _, currState = heapq.heappop(unvisited)

        # Goal check
        if reachGoal(currState.grid):
            return currState

        # Track most balanced option
        weightVal = abs(left(currState.grid) - right(currState.grid))
        if weightVal < minWeight:
            minWeight = weightVal
            minState = currState

        # Generate neighbors
        nextMoves = computeMoves(currState)  

        for neighbor in nextMoves:
            neighbor_tuple = grid_to_tuple(neighbor.grid)
            new_cost = neighbor.time  # your computeHeuristic already uses time

            # Add neighbor if not visited or if this path is faster (lower time)
            if neighbor_tuple not in cost_so_far or new_cost < cost_so_far[neighbor_tuple]:
                cost_so_far[neighbor_tuple] = new_cost
                neighbor.parent = currState
                priority = computeHeuristic(neighbor)
                heapq.heappush(unvisited, (priority, next(counter), neighbor))
    return minState


def updateManifest(goalGrid, manifestName):
    name, ext = manifestName.rsplit(".", 1)
    newFile = name + "OUTBOUND." + ext
    with open(newFile, "w") as f:
        for i in range(1,9):
            for j in range(1,13):
                container = goalGrid[i][j]
                contWeight = str(container[0]).zfill(5)
                row = str(i).zfill(2)
                col = str(j).zfill(2)
                f.write(f"[{row},{col}], {{{contWeight}}}, {container[1]}\n")

def manhattan(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

def printGridWithBalance(grid, title="Ship Grid"):
    """
    Prints the ship grid with bottom-left as (1,1) and shows left/right weights.
    """
    print(f"\n=== {title} ===")

    # Print column numbers
    col_nums = ["{:>4}".format(j) for j in range(1, 13)]
    print("     " + " ".join(col_nums))  # extra space for row numbers

    # Print the grid from bottom row to top row
    for i in range(8, 0, -1):  # row 8 at top, row 1 at bottom
        row_display = []
        for j in range(1, 13):
            weight, contents = grid[i][j]
            if contents == "NAN":  # blocked spot
                row_display.append("####")
            elif weight == 0:      # empty spot
                row_display.append("----")
            else:                  # container with weight
                row_display.append(str(weight).zfill(4))
        print("{:>3} | ".format(i) + " | ".join(row_display))
    
    # Calculate left/right weights
    left_weight = sum(grid[i][j][0] for i in range(1,9) for j in range(1, 13//2 + 1) if grid[i][j][1] != "NAN")
    right_weight = sum(grid[i][j][0] for i in range(1,9) for j in range(13//2 + 1, 13) if grid[i][j][1] != "NAN")
    
    print("\nLeft Side Weight : ", left_weight)
    print("Right Side Weight: ", right_weight)
    print("Difference      : ", abs(left_weight - right_weight))
    print("="*70 + "\n")
def computeHeuristic(currState):
    time = currState.time 
    absDiff = abs(left(currState.grid) - right(currState.grid))
    return time + absDiff

def backtrack(currState, start):
    path = []
    while currState != start:
        path.append(currState)
        currState = currState.parent
    path.append(start)
    path.reverse()

    with open("Moves.txt", "w") as f:
        for state in path:
            f.write(print_grid(state.grid) + "\n\n")  # write the grid string to file


def print_grid(grid):
    """
    grid: 9x13 list of tuples (weight, contents)
    Prints the grid with weights only, row 1 at the bottom.
    """
    rows = len(grid)
    cols = len(grid[0])

    lines = []
    for i in range(rows-1, -1, -1):  # start from bottom row
        row_str = ""
        for j in range(cols):
            weight = grid[i][j][0]  # get the weight
            row_str += f"{weight:3} "  # pad for alignment
        lines.append(row_str)
    
    # Combine all rows into a single string
    grid_str = "\n".join(lines)
    return grid_str 


















