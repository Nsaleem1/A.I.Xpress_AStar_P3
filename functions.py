import copy
from collections import deque
import heapq
from itertools import count
from datetime import datetime

def timestamp_now():
    return datetime.now()

def timestamp_string(dt=None):
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%m %d %Y: %H:%M")

# container class, each cont has a loc, weight, and contents section
class Container:
    def __init__(self, location, weight, contents):
        self.location = location
        self.weight = weight
        self.contents = contents
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
    if abs(leftVal - rightVal) <= (sum([leftVal, rightVal]) * 0.10):
        return True
    return False

def newState(oldRow, oldCol, newRow, newCol, currState):
    grid = copy.deepcopy(currState.grid)   

    value, content = grid[oldRow][oldCol]
    time = manhattan((oldRow, oldCol), (newRow, newCol), grid) + currState.time
    
    grid[oldRow][oldCol] = (0, "UNUSED")
    grid[newRow][newCol] = (value, content)

    

    return state(grid, left(grid), right(grid), reachGoal(grid), time, currState)

# need to go to UNUSED spot
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

            # this container is on the top since above it is UNUSED, and container itself cant be  NAN
            # need the i == 8 check since i + 1 be out of bounds for top row

            # very top row
            if (i == 8 and grid[i][j][1] != "UNUSED" and grid[i][j][1] != "NAN"):    
                # find an empty spot
                for row in range (1,9):
                    for col in range (1,13):
                        if (grid[row][col][1] == "UNUSED" and grid[row][col][1] != "NAN" and not (col in checkedCol)):
                            nextStates.append(newState(i, j, row, col, copy.deepcopy(state)))
                            checkedCol.append(col)

            # moving only containers with nothing above
            elif ((i < 8) and (grid[i+1][j][1] == "UNUSED") and (grid[i][j][1] != "UNUSED") and (grid[i][j][1] != "NAN")):
                for row in range (1,9):
                    for col in range (1,13):
                        if (grid[row][col][1] == "UNUSED" and grid[row][col][1] != "NAN" and not (col in checkedCol)):
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

# my heuristic is time + diff in weights
# choosing the move with less time and makes more balanced 
def AStar(start):
    counter = count()
    unvisited = []
    minWeight = float('inf')
    heapq.heappush(unvisited, (computeHeuristic(start), next(counter), start))

    grid_to_tuple = lambda g: tuple(tuple(row) for row in g)
    #stores best so far cost of each grid 
    cost_so_far = {grid_to_tuple(start.grid): start.time}

    while unvisited:
        _, _, currState = heapq.heappop(unvisited)

        # Goal check
        if reachGoal(currState.grid):
            return currState

        # Generate neighbors
        nextMoves = computeMoves(currState)  

        for neighbor in nextMoves:
            neighbor_tuple = grid_to_tuple(neighbor.grid)
            newCost = neighbor.time  

            # Add neighbor if not visited or if this path is faster (lower time)
            if neighbor_tuple not in cost_so_far or newCost < cost_so_far[neighbor_tuple]:
                cost_so_far[neighbor_tuple] = newCost
                neighbor.parent = currState
                fValue = newCost + computeHeuristic(neighbor)
                heapq.heappush(unvisited, (fValue, next(counter), neighbor))
        
        # Track most balanced option. If weights are equal, prioritize the cheaper path (lower time).
        weightVal = abs(left(currState.grid) - right(currState.grid))
        if weightVal < minWeight or (weightVal == minWeight and currState.time < minState.time):
            minWeight = weightVal
            minState = currState

    return minState

def computeHeuristic2(neighbor):
    grid = neighbor.grid
    maxWeight = 0
    value = 0
    tr = 1
    tc = 1
    
    # state that frees the heaviest container is prioritized
     
    #find heaviest container 
    for r in range(1,9):
        for c in range(1, 13):
            weight , _ = grid[r][c]
            if weight > maxWeight:
                maxWeight = weight
                tr = r
                tc = c
    # the more containers on the top of the heaviest is bad
    for i in range (tr+1,9):
        if grid[i][tc][1] != "UNUSED":
            value += 1
    
    return value
                    

# heuristic is trying to move the heaviest container 
def AStar2(start):
    counter = count()
    unvisited = []
    minWeight = float('inf')
    heapq.heappush(unvisited, (computeHeuristic(start), next(counter), start))

    grid_to_tuple = lambda g: tuple(tuple(row) for row in g)
    #stores best so far cost of each grid 
    cost_so_far = {grid_to_tuple(start.grid): start.time}

    while unvisited:
        _, _, currState = heapq.heappop(unvisited)

        # Goal check
        if reachGoal(currState.grid):
            return currState

        # Generate neighbors
        nextMoves = computeMoves(currState)  

        for neighbor in nextMoves:
            neighbor_tuple = grid_to_tuple(neighbor.grid)
            newCost = neighbor.time  

            # Add neighbor if not visited or if this path is faster (lower time)
            if neighbor_tuple not in cost_so_far or newCost < cost_so_far[neighbor_tuple]:
                cost_so_far[neighbor_tuple] = newCost
                neighbor.parent = currState
                fValue = newCost + computeHeuristic2(neighbor)
                heapq.heappush(unvisited, (fValue, next(counter), neighbor))
        
        # Track most balanced option. If weights are equal, prioritize the cheaper path (lower time).
        weightVal = abs(left(currState.grid) - right(currState.grid))
        if weightVal < minWeight or (weightVal == minWeight and currState.time < minState.time):
            minWeight = weightVal
            minState = currState

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

def availablePos(grid, r, c):
    return grid[r][c][1] == "UNUSED" 

def manhattan(loc1, loc2, grid):
    r,c = loc1
    tr, tc = loc2
    distance = 0

    if loc1 == (8,1) or loc2 == (8,1):
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])
    
    # horizontal alignment
    while c != tc:

        #go right
        if tc > c:
            if availablePos(grid, r, c+1):
                c += 1
            #go up if not
            else:
                r += 1
        
        #go left
        elif tc < c:
            if availablePos(grid, r, c-1):
                c -= 1
            #go up if not
            else:
                r += 1

        distance += 1
    
    #vertical alignment
    while r != tr:
        r -= 1
        distance += 1
    
    return distance

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

    with open("Moves.txt", "a") as f:
        #write down the moves
        for i in range(len(path) - 1):
            grid1 = path[i].grid
            grid2 = path[i+1].grid
            gridAction = getAction(grid1, grid2)
            f.write(f"{gridAction}\n")

        for state in path:
            f.write(printGrid(state.grid) + "\n\n") 

def printGrid(grid):

    rows = len(grid)
    cols = len(grid[0])

    lines = []
    # start from bottom row
    for i in range(rows-1, -1, -1):  
        row_str = ""
        for j in range(cols):
            weight = grid[i][j][0]  
            # padding
            row_str += f"{weight:3} "  
        lines.append(row_str)
    
    # Combine all rows into a single string
    grid_str = "\n".join(lines)
    return grid_str 

def getAction(grid1, grid2):
    old_pos = None
    new_pos = None
    moved_container = None

    for r in range(9):
        for c in range(13):
            w1, name1 = grid1[r][c]
            w2, name2 = grid2[r][c]

            # Container disappeared → old position
            if name1 != "UNUSED" and name2 == "UNUSED":
                old_pos = (r, c)
                moved_container = name1

            # Container appeared → new position
            if name1 == "UNUSED" and name2 != "UNUSED":
                new_pos = (r, c)

    if moved_container and old_pos and new_pos:
            old_str = f"[{old_pos[0]:02d}, {old_pos[1]:02d}]"
            new_str = f"[{new_pos[0]:02d}, {new_pos[1]:02d}]"
            duration = manhattan(old_pos, new_pos, grid1)
            return f'Move {moved_container} from {old_str} to {new_str}, {duration} minute(s)'
    return "no single move detected"

def getMovedContainer(grid1, grid2):
    old_pos = None
    new_pos = None
    moved_container = None

    for r in range(9):
        for c in range(13):
            w1, name1 = grid1[r][c]
            w2, name2 = grid2[r][c]

            # Container disappeared → old position
            if name1 != "UNUSED" and name2 == "UNUSED":
                old_pos = (r, c)
                moved_container = name1

            # Container appeared → new position
            if name1 == "UNUSED" and name2 != "UNUSED":
                new_pos = (r, c)

    return moved_container, old_pos, new_pos
    
def craneToGrid(initialGrid, secondGrid):
    movedContainer, pos, _ = getMovedContainer(initialGrid, secondGrid)
    time = manhattan((8,1), pos, initialGrid)
    return time, movedContainer, pos

def gridToCrane(beforeLastGrid, lastGrid):
    movedContainer, _, pos = getMovedContainer(beforeLastGrid, lastGrid)
    time = manhattan((8,1), pos, lastGrid)
    return time, movedContainer, pos

def secondStates(goalState):
    secondToLastState = goalState.parent

    # find the second state
    prevState = goalState.parent
    currState = goalState
    while prevState.parent is not None:
        currState = currState.parent
        prevState = prevState.parent

    return currState, secondToLastState, prevState

def totalTime(goalState):
    second, beforeLast, start = secondStates(goalState)
    craneGrid, _, _ = craneToGrid(start.grid, second.grid)
    gridCrane, _, _ = gridToCrane(beforeLast.grid, goalState.grid)
    total = goalState.time + craneGrid + gridCrane
    return total












