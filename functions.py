import math
import matplotlib.pyplot as plt
import random
import copy
from collections import deque
import os

class state:
    def __init__(self, grid, left, right, goal):
        self.grid = grid
        self.left = left
        self.right = right
        self.goal = goal 

#ship grid, contains the grid with a grid object
# grid object has weight,content 
def shipGrid(containers):
    #create a matrix 9 x 13 (one more since manifest not start at (0,0))
    grid = [[(0,"NAN") for _ in range(13)] for _ in range(9)]
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


def newState(oldRow, oldCol, newRow, newCol, grid):

    value = grid[oldRow][oldCol][0]
    content = grid[oldRow][oldCol][1]

    #empty curr location
    grid[oldRow][oldCol] = (0, "UNUSED")
    #add to new loc
    grid[newRow][newCol] = (value, content)

    return state(grid, left(grid), right(grid), reachGoal(grid))

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
                        if (grid[row][col] == 0 and not (col in checkedCol)):
                            nextStates.append(newState(i, j, row, col, copy.deepcopy(grid)))
                            checkedCol.append(col)

            elif (i < 8 and grid[i+1][j][0] == 0 and grid[i][j][0] != 0 and grid[i][j][1] != "NAN"):
                for row in range (1,9):
                    for col in range (1,13):
                        if (grid[row][col] == 0 and not (col in checkedCol)):
                            nextStates.append(newState(i, j, row, col, copy.deepcopy(grid)))
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
    unvisited = deque()
    unvisited.append(start)
    visited = set()
   
    while unvisited:
        #select state from queue, get its next states, add to visited
        currState = unvisited.popleft()
        nextMoves = computeMoves(copy.deepcopy(currState))

        #PROBLEM FOR TEST I PRINT NEXT MOVES AND I GET 0 ?? should be 66 for the first state
        print(len(nextMoves))
        
        goal = reachGoal(currState.grid)
        visited.add(currState)

        #if its goal, we are done
        if goal:
            return currState

        #else calculate next states
        for next in nextMoves:
            if(next not in visited):
                unvisited.append(next)
        

        #keep track of most balanced option too 
        weightVal = left(currState.grid) - right(currState.grid)
        if weightVal < minWeight:
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
                contWeight = str(container[0]).zfill(4)
                row = str(i).zfill(2)
                col = str(j).zfill(2)
                f.write(f"[{row}, {col}], {{{contWeight}}}, {container[1]}\n")













