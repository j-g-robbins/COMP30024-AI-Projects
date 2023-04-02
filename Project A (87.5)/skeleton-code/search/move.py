# To print all upper tokens and their moves:
#  for token in tokenMoves(data):
    # print(token, tokenMoves(data)[token])

UPPER = "upper"
LOWER = "lower"
BLOCKER = "block"
TYPE = 0
R = 1
Q = 2
BOARD_LEN = 8
BOARD_LIMIT = 4
ROCK = 'r'
PAPER = 'p'
SCISSORS = 's'


# Calculate the number of tiles distance between two tokens
def coordDistance(upper, lower):
    node = (lower[R] - upper[R]), (lower[Q] - upper[Q])
    if (((node[0] < 0) & (node[1] > 0)) | ((node[0] > 0) & (node[1] < 0))):
        distance = max(abs(node[0]), abs(node[1]))
    else:
        distance = abs(node[0]) + abs(node[1])
    return distance

# Return all valid moves for an upper token ########## Need to edit to include lower for strategy later
def tokenMoves(board):
    moves = {}
    for token1 in board[UPPER]:
        moves[token1[R], token1[Q]] = set()
        for cand in adjacentTiles(token1, board[BLOCKER]):
            moves[token1[R], token1[Q]].add(cand)
        for token2 in board[UPPER]:
            if ((token1[R], token1[Q]) != (token2[R], token2[Q])):
                for cand in swingMoves(token1, token2, board):
                    moves[token1[R], token1[Q]].add(cand)
    return moves

# Return a set of the valid swing moves for a token adjacent to another token
def swingMoves(token1, token2, board):
    moves = set()
    if (coordDistance(token1, token2) == 1):
        for move in adjacentTiles(token2, board[BLOCKER]): # need to append adjacent non-block tiles, adjacentTiles function
            if ((move[0], move[1]) != (token1[R], token1[Q])):
                moves.add(move)
    return moves

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
                if not onBoard(("", (token[R]+i), (token[Q] + j))):
                    movable = False
                if (movable):
                    tiles.append((token[R]+i, token[Q]+j))
    return tiles

"""# Return coordinatees of all adjacent tiles to a token that are not blockers 
def adjacentTiles(token, blockers):
    tiles = []
    for i in range(-1, 2):
        for j in range(-1, 2): 
            if (i != j):
                movable = True
                for blocker in blockers:
                    if ((token[R]+i == blocker[R]) & (token[Q]+j == blocker[Q])):
                        movable = False
                if ((abs(token[R] + i) > BOARD_LIMIT) | (abs(token[Q] + j) > BOARD_LIMIT)):
                    movable = False
                if (movable):
                    tiles.append((token[R]+i, token[Q]+j))
    return tiles"""

# Return dictionary mapping each upper token to the closest lower node by distance
def closestNodes(board):
    closestNodes = {}
    for upper in board[UPPER]:
        closest = BOARD_LEN + 1
        
        for lower in board[LOWER]:
            if (coordDistance(upper, lower) < closest):
                closest = coordDistance(upper, lower)
                closestNodes[upper[0], upper[R], upper[Q]] = lower
    return closestNodes

def compareTokens(token1, token2):
    if (token1[TYPE] == token2[TYPE]):
        return 0
    elif (token1[TYPE] == ROCK):
        if (token2[TYPE] == SCISSORS):
            return 1
        return -1
    elif (token1[TYPE] == SCISSORS):
        if (token2[TYPE] == PAPER):
            return 1
        return -1
    else:
        if (token2[TYPE] == ROCK):
            return 1
        return -1

# Return dictionary with key for each upper token
# and value the distance to the closest token it
# can eliminate
def closestCanKill(board):

    distance = 0
    closestNodes = {}

    for upper in board[UPPER]:
        closest = BOARD_LEN + 1 # does not add to heuristic if has no corresponding nodes
        target = False
        
        for lower in board[LOWER]:
            if (compareTokens(upper, lower) == 1):
                target = True
                distance = coordDistance(upper, lower)
                if (distance < closest):
                    if (compareTokens(upper, lower) == 1):
                        closest = distance
                        closestNodes[upper[0], upper[R], upper[Q]] = distance
        if not target:
            closestNodes[upper[0], upper[R], upper[Q]] = 0

        """for lower in board[LOWER]:
            distance = coordDistance(upper, lower)
            if (distance < closest):
                if (compareTokens(upper, lower) == 1):
                    closest = distance
                    closestNodes[upper[0], upper[R], upper[Q]] = distance"""
    return closestNodes