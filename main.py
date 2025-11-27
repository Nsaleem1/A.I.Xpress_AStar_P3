import math
import random
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
#from zoneinfo import ZoneInfo
import functions
from dataclasses import dataclass

manifestName = input("Enter the manifest: ")
containers = []

# container class, each cont has a loc, weight, and contents section
class Container:
    def __init__(self, location, weight, contents):
        self.location = location
        self.weight = weight
        self.contents = contents

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
        #weight = int(part2)

        # third part is contents - str
        contents = parts[2]
        if contents == "NAN":
            contents = None
        container = Container(location, weight, contents)
        containers.append(container)

grid = functions.shipGrid(containers)
left = functions.left(grid)
right = functions.right(grid)
goal = functions.reachGoal(left, right)
initialState = functions.state(grid, left, right, goal)
nextMoves = functions.computeMoves(initialState)


#i think this should be like 66 
print(len(nextMoves))

#PROGRESS SO FAR:
# need to fix compute moves, i think it should be 66 next moves but also not confident of that number 
# so all the next moves from a state is like every container that u can place where that spot is 0
# BUT, must have something below and can not be above urself 
# to take care of the something below I js did a checkedCol thing bc we work from bottom up 
# so if i alr checked a space cus it was empty then that whole col is good 


#NOTES:
# dw abt Astar lets just do BFS and then we can try to figure out the heuristic 
# if that is easier idk 
# oh and same with tracking the time it takes we can probs js add that later


# function general-search(problem, QUEUEING-FUNCTION)
# nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
# loop do
# if EMPTY(nodes) then return "failure" (we have proved there is no solution!)
# node = REMOVE-FRONT(nodes)
# if problem.GOAL-TEST(node.STATE) succeeds then return node
# nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
# end