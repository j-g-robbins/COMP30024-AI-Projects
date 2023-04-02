""" This module contains functions for displaying the output
of the AI """

from search.move import coordDistance

UPPER = "upper"
LOWER = "lower"
BLOCK = "block"
BLOCK_TOKEN = "|B|"
TOKEN = 0
R = 1
Q = 2
ROCK = 'r'
PAPER = 'p'
SCISSORS = 's'
SLIDE = "SLIDE"
SWING = "SWING"

def evaluateBoard(board):
    # given a board state determines if any tiles are
    # on the same hex and evaluates which are deleted
    
    delete = []
    tokens = dict()
    upper = board[UPPER]
    upperMax = len(upper)
    lower = board[LOWER]
    lowerMax = len(upper) + len(lower)
    full = upper + lower
    
    # adds all tokens in the same position to a dictionary
    # and then adds the indices of tokens that should
    # be deleted to a set
    for i in range(lowerMax):
        tokens = {}
        tokens[full[i][TOKEN]] = [i]
        for j in range(i + 1, lowerMax):
            if full[i][R:Q+1] == full[j][R:Q+1]:
                if full[j][TOKEN] not in tokens:
                    tokens[full[j][TOKEN]] = [j]
                else:
                    tokens[full[j][TOKEN]].append(j)
        delete = delete + fight(tokens)

    # converting delete from list of lists to single list
    newDelete = []
    for token in delete:
        for position in token:
            newDelete.append(position)
    delete = newDelete

    # creating output board excluding elements that should
    # be deleted 
    newBoard = dict()
    newBoard[UPPER] = []
    newBoard[LOWER] = []
    newBoard[BLOCK] = board[BLOCK]
    i = 0
    while i < upperMax:
        if i in delete:
            i = i + 1
            continue
        newBoard[UPPER].append(board[UPPER][i])
        i = i + 1
    while i < lowerMax:
        if i in delete:
            i = i + 1
            continue
        newBoard[LOWER].append(board[LOWER][i - upperMax])
        i = i + 1

    return newBoard

def fight(tokens):
    # takes a dictionary of tokens as key and positions
    # in a full list of tokens as values, returns 
    # a list of the positions in the full list that
    # need to be deleted

    if (ROCK in tokens) and (PAPER in tokens) and (SCISSORS in tokens):
        delete = [tokens[ROCK]] + [tokens[PAPER]] + [tokens[SCISSORS]]
    elif (ROCK in tokens) and (PAPER in tokens):
        delete = [tokens[ROCK]]
    elif (ROCK in tokens) and (SCISSORS in tokens):
        delete = [tokens[SCISSORS]]
    elif (PAPER in tokens) and (SCISSORS in tokens):
        delete = [tokens[PAPER]]
    else:
        delete = []
    
    return delete

def convertInput(rawBoardDict):
    """ Takes raw json file and converts it to a format that can
    be read by the print board function. """

    boardDict = {} # Dictionary that can be read by print board function

    # iterating through all pieces under each key in the dictionary
    # so they are in a usable format
    pieceType = ""
    for key in rawBoardDict:
        for piece in rawBoardDict[key]:
            if key == UPPER:
                pieceType = piece[TOKEN].upper()
            elif key == "":
                pieceType = BLOCK_TOKEN
            else:
                pieceType = piece[TOKEN]
            boardDict[(piece[R], piece[Q])] = '(' + pieceType + ')'

    return boardDict

def printOutput(board1, board2, turn):
    tokenInit = tokenFinal = moveType = []
    for token1 in board1[UPPER]:
        if (token1 not in board2[UPPER]):
            for token2 in board2[UPPER]:
                if (token2 not in board1[UPPER]):
                    if ((coordDistance(token1, token2) <= 2) \
                        and (token1[TOKEN] == token2[TOKEN])):
                        tokenInit.append(token1)
                        tokenFinal.append(token2)
                        if (coordDistance(token1, token2) == 1):
                            moveType.append(SLIDE)
                        else:
                            moveType.append(SWING)
    
    for i in range(len(tokenInit)):
        print("Turn {}: {} from ({},{}) to ({},{})".format(turn, \
        moveType, tokenInit[i][R], tokenInit[i][Q], tokenFinal[i][R], tokenFinal[i][Q]))