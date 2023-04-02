ROCK = 'r'
PAPER = 'p'
SCISSORS = 's'

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
        closest = BOARD_LEN + 1
        
        for lower in board[LOWER]:
            distance = coordDistance(upper, lower)
            if (distance < closest):
                if (compareTokens(upper, lower) == 1):
                    closest = distance
                    closestNodes[upper[0], upper[R], upper[Q]] = distance
    return closestNodes