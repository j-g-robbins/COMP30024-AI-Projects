""" This module contains basic tree functions
necessary to build our tree and create nodes """

"""class node:
    # a node representing a hex on the board
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        self.children = []
        self.g = 0
        self.h = 0
        self.f = 0

    def appendNode(self, data):
        # inserts a node as a child to the
        # current node and returns the child node
        newNode = node(self, data)
        self.children.append(newNode)
        return newNode

    def __lt__(self, other):
        if self.f < other.f:
            return -1
        elif self.f == other.f:
            return 0
        return 1"""

# standard library
from collections import deque
import copy
from itertools import product
import heapq

# team files
from search.move import tokenMoves, closestCanKill
from search.output import evaluateBoard

UPPER = "upper"
LOWER = "lower"
TYPE = 0
R = 1
Q = 2
NEWLINE = '\n'

class node:
    # a node representing a hex on the board
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        self.children = []
        self.g = 0
        if parent:
            self.g = parent.g + 1
        self.h = heuristic(self.data)
        self.f = self.g + self.h

    def appendNode(self, data):
        # inserts a node as a child to the
        # current node and returns the child node
        newNode = node(self, data)
        newNode.g = self.g + 1
        self.children.append(newNode)
        return newNode

    def __lt__(self, other):
        if self.f < other.f:
            return -1
        elif self.f == other.f:
            return 0
        return 1

class tree:
    # a tree containing a root node and
    # functions for initialising and
    # traversing
    def __init__(self, data):
        self.root = node(None, data)

    def printTree(self):
        # takes tree root as input and prints the tree
        # with breadth-first traversal

        # initialising queue
        queue = deque()
        queue.append(self.root)
        queue.append(NEWLINE)
        
        # printing nodes in queue adding newlines at each level
        while queue:
            current = queue.popleft()
            if current == NEWLINE:
                if queue:
                    queue.append(NEWLINE)
                print(NEWLINE, end = '')
            else:
                for child in current.children:
                    queue.append(child)
                print(current.data, ' ', end = '')

    def bfs(self, initialState):
        # uses breadth-first search to work out the shortest
        # path from the start hex to the final hex

        queue = []
        queue.append(self.root)
        visited = set()
        visited.add(str(initialState))
        while queue:
            current = heapq.heappop(queue)
            current.data = evaluateBoard(current.data)
            if current.data[LOWER] == []: # goal state
                return(generateSolution(current))
            children = newStates(current, visited)
            for child in children:
                #if child.f <= current.f:
                heapq.heappush(queue, child)
        """queue = deque()
        queue.append(self.root)
        visited = set()
        visited.add(str(initialState))
        while queue:
            current = queue.popleft()
            current.data = evaluateBoard(current.data)
            if current.data[LOWER] == []: # goal state 
                return(generateSolution(current))
            children = newStates(current, visited)
            for child in children:
                queue.append(child)"""

def generateSolution(node):
    # traverses the tree from the specified node to the root
    # adding items to a solution stack so that the top item
    # is the first move to reach the goal state

    solution = deque()
    while node:
        solution.append(node.data)
        node = node.parent
    
    return solution

def newStates(node, visited):
    # convert tokenMoves output into new board states
    # and returns them as nodes in a list to be added
    # to BFS queue
    
    children = []

    # creating all combinations of moves for each token
    # and converting tokenMoves() output into a format 
    # readable by the product() function
    tokens = tokenMoves(node.data)
    numTokens = len(tokens)
    movesList = [list(tokens[token]) for token in tokens]
    moveCombinations = list(product(*movesList))

    # looping through list of all move combinations to
    # create new board states
    for moveCombination in moveCombinations:
        newState = copy.deepcopy(node.data)
        for i in range(numTokens):
            newState[UPPER][i] = list(newState[UPPER][i][TYPE]) + list(moveCombination[i])
            if str(newState) not in visited:
                visited.add(str(newState))
                current = node.appendNode(newState)
                children.append(current)
    return children

"""def heuristic(board):
    # takes data as input and returns a
    # heuristic value to be used by BFS

    return len(board[LOWER])"""

def heuristic(board):

    minDistanceDict = closestCanKill(board)
    minDistanceList = [minDistanceDict[token] for token in minDistanceDict]
    
    if minDistanceList:
        return max(minDistanceList)

    return 0

    """def aStar(self, initialState, goal):
        # uses breadth-first search to work out the shortest
        # path from the start hex to the final hex

        queue = []
        queue.append(self.root)
        heapq.heapify(queue)
        visited = set()
        visited.add(str(initialState))
        while queue:
            current = heapq.heappop(queue)
            current.h = heuristic(current.data, UPPER)
            current.f = current.g + current.h
            if current.data == goal:
                current.data = evaluateBoard(current.data) ### might need to move to a different stage 
                ### in course conflict also occurs during search
                return(generateSolution(current))
            children = newStates(current, visited)
            for child in children:
                child.g = current.g + 1
                child.h = heuristic(child.data, UPPER)
                child.f = child.g + child.h
                if (child.f <= current.f):
                    heapq.heappush(queue, child)"""