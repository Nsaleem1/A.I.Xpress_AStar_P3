import math
import matplotlib.pyplot as plt
import random
import copy
import os

class state:
    def __init__(self, grid, left, right, goal):
        self.grid = grid
        self.left = left
        self.right = right
        self.goal = goal 

#ship grid, contains the grid with either container weight in the spot or None
def shipGrid(containers):
    #create a matrix 9 x 13 (one more since manifest not start at (0,0))
    grid = [[0 for _ in range(13)] for _ in range(9)]
    for container in containers:
        row,col = container.location
        if container.contents == None:
            grid[row][col] = None
        else:
            grid[row][col] = int(container.weight)
    return grid

#should be fine if I transverse the extra row of 0,0 since the values are 0 i think
def left(grid):
    totalWeight = 0
    for i in range(9):
        for j in range(13 // 2 + 1):
            if grid[i][j] != None:
                totalWeight += grid[i][j]
    return totalWeight

#should be fine if I transverse the extra row of 0,0 since the values are 0 i think
def right(grid):
    totalWeight = 0
    for i in range(9):
        for j in range(13 // 2 + 1, 13):
            if grid[i][j] != None:
                totalWeight += grid[i][j]
    return totalWeight

def reachGoal(left, right):
    #need to add the or reach minimal stuff otherwise if the test case never reach this condition
    # it will be infinite loop
    if ((left - right) < (sum([left, right]) * 0.10)):
        return True
    return False


def newState(oldRow, oldCol, newRow, newCol, grid):
    value = grid[oldRow][oldCol]
    grid[oldRow][oldCol] = 0
    grid[newRow][newCol] = value
    return state(grid, left(grid), right(grid), reachGoal(left(grid), right(grid)))

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

            if (i == 8 and grid[i][j] != 0 and grid[i][j] != None):    
                # find an empty spot
                for row in range (1,9):
                    for col in range (1,13):
                        if (grid[row][col] == 0 and not (col in checkedCol)):
                            nextStates.append(newState(i, j, row, col, copy.deepcopy(grid)))
                            checkedCol.append(col)

            elif (i < 8 and grid[i+1][j] == 0 and grid[i][j] != 0 and grid[i][j] != None):
                for row in range (1,9):
                    for col in range (1,13):
                        if (grid[row][col] == 0 and not (col in checkedCol)):
                            nextStates.append(newState(i, j, row, col, copy.deepcopy(grid)))
                            checkedCol.append(col)
    return nextStates








