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
        # if contents == "NAN":
        #     contents = None
        container = Container(location, weight, contents)
        containers.append(container)

#creating start state
grid = functions.shipGrid(containers)
left = functions.left(grid)
right = functions.right(grid)
goal = functions.reachGoal(grid)
initialState = functions.state(grid, left, right, goal)

#see if it is an edge case, else run regular BFS
foundGoal = initialState
isEdge = functions.edgeCase(initialState , containers)
if not isEdge:
    foundGoal = functions.BFS(initialState)

functions.updateManifest(foundGoal.grid, manifestName)
print("Proram was successful. See Updated Manifest.")


#PROGRESS SO FAR:
# completed BFS approach, but I m getting logic error look at BFS function
# need to check my functions

#NOTES:
# include time, maybe computeTime function or sum 
# make it a star 


