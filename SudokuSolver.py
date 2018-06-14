from multiprocessing import Queue
import copy

class Board(object):

    def __init__(self, initial):
        self.initial = initial
        self.type = 9
        self.height = int(self.type/3)

    # Return all moves that havent been made
    def possibleMoves(self, vals, used):
        return [num for num in vals if num not in used]

    # Return first 0 on the Board
    def getMove(self, board, state):
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column   

    def actions(self, state):
        nums = range(1, self.type+1)
        #Values this state can be in its column
        columnVals = []
        #Values this state can be in its square
        squareVals = []

        row,column = self.getMove(self.type, state)

        #Values this state can be in its row
        rowVals = [num for num in state[row] if (num != 0)]
        #Starting list of possibleMoves based soley on rows
        options = self.possibleMoves(nums, rowVals)

        #Get current values in this column
        for currCol in range(self.type):
            if state[currCol][column] != 0:
                columnVals.append(state[currCol][column])
        #Remove possibleMoves based on column
        options = self.possibleMoves(options, columnVals)

        currRow = int(row/self.height)*self.height
        currCol = int(column/3)*3

        #Get current values in this square
        for squareRow in range(0, self.height):
            for squareCol in range(0,3):
                squareVals.append(state[currRow + squareRow][currCol + squareCol])
        ##Remove possibleMoves based on square
        options = self.possibleMoves(options, squareVals)

        for number in options:
            yield number, row, column      

    # Returns updated board after adding new valid value
    def newBoard(self, state, action):

        thisState = action[0]
        thisRow = action[1]
        thisColumn = action[2]

        #Put new value into a new board and return that board
        newB = copy.deepcopy(state)
        newB[thisRow][thisColumn] = thisState

        return newB

    # Test if the board is complete 
    def goal(self, state):

        #Sum of a complete section
        total = sum(range(1, self.type+1))

        #Check if rows/cols are all completed with 1-9 only
        for row in range(self.type):
            if (len(state[row]) != self.type) or (sum(state[row]) != total):
                return False

            colTot = 0
            for col in range(self.type):
                colTot += state[col][row]

            if (colTot != total):
                return False

        #Check if squares are all completed with 1-9 only
        #Used to iterate through the whole board
        for col in range(0,self.type,3):
            for row in range(0,self.type,self.height):

                #Used to iterate through a particular square
                squareTot = 0
                for squareRow in range(0,self.height):
                    for squareCol in range(0,3):
                        squareTot += state[row + squareRow][col + squareCol]

                if (squareTot != total):
                    return False

        return True

class currBoard:

    def __init__(self, state, move=None):
        self.state = state
        self.move = move

    # Each action will create a new set of states  
    def moves(self, board):
        return [self.childStates(board, move)
                for move in board.actions(self.state)]

    # Returns a new board for a given move 
    def childStates(self, board, move):
        next = board.newBoard(self.state, move)
        return currBoard(next, move)

def BFS(board):
    curr = currBoard(board.initial)
    print "Starting board:"
    for row in curr.state:
                print (row)
    # Check if board is solved already
    if board.goal(curr.state):
        return curr

    frontier = Queue()
    frontier.put(curr)
    iterations = 0
    
    # Continuously generate new moves using BFS until either
    # A solution is found or there are no more moves
    while (frontier.qsize() != 0):

        iterations += 1
        curr = frontier.get()
        if iterations % 500 == 0:
            print "Current board:"
            for row in curr.state:
                print (row)
        
        for child in curr.moves(board):
            #If one of the children is a goal state return it
            if board.goal(child.state):
                return child, iterations
            #Otherwise push the child onto the frontier 
            frontier.put(child)

    return None, iterations

def solveBoard(board):
    solution, i = BFS(Board(testBoard))
    print i, " iterations to solve."
    print "Solved Board:"
    for row in solution.state:
            print (row)

#---------------- Testing the solver here

testBoard = [[0,0,0,8,4,0,6,5,0],
      [0,8,0,0,0,0,0,0,9],
      [0,0,0,0,0,5,2,0,1],
      [0,3,4,0,7,0,5,0,6],
      [0,6,0,2,5,1,0,3,0],
      [5,0,9,0,6,0,7,2,0],
      [1,0,8,5,0,0,0,0,0],
      [6,0,0,0,0,0,0,4,0],
      [0,5,2,0,8,6,0,0,0]]
solveBoard(testBoard)
