def onBoard(token):
    if (coordDistance(("", 0, 0), token) > 4):
        return False
    return True


# Return coordinatees of all adjacent tiles to a token that are not blockers 
def adjacentTiles(token, blockers):
    tiles = []
    for i in range(-1, 2):
        for j in range(-1, 2): 
            if (i != j):
                movable = True
                for blocker in blockers:
                    if ((token[R]+i == blocker[R]) & (token[Q]+j == blocker[Q])):
                        movable = False
                if (~onBoard(("", (token[R]+i), (token[Q] + j)))):
                    movable = False
                if (movable):
                    tiles.append((token[R]+i, token[Q]+j))
    return tiles