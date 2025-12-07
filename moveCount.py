def moveCount(goal_state):
    if goal_state is None:
        return []

    path = []
    curr = goal_state
    while curr is not None:
        path.append(curr)
        curr = curr.parent

    path.reverse() 
    moves = len(path) - 1
    return moves

