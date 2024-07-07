# Input of board array. Prints the board
def printBoard(board):
    for row in board:
        for col in row:
            print(col, end = " ")
        print()

# Copies the board array. This is to avoid pointer problems >:(
def copyList(list):
    newList = []
    for item in list:
        newList.append(item)
    return newList

def copyBoard(board):
    newBoard = []
    for row in board:
        newBoard.append(copyList(row))
    return newBoard

# returns a 2 index array
# 1st index: True/False game over boolean
# 2nd index:
# - if game is over, 1 means X won, -1 means O won, 0 means tie
# - otherwise, it'll just be 0 (irrelevant)

def gameOver(board):
    retList = [False, 0]

    # keep track of blank spaces to detect a tie
    blanks = 0

    # check for wins in the rows
    for row in board:
        Xcounter = 0
        Ocounter = 0
        for col in row:
            if col == "X":
                Xcounter += 1
            elif col == "O":
                Ocounter += 1
            else:
                blanks += 1
                break
        if Xcounter == 3:
            return [True, 1]
        elif Ocounter == 3:
            return [True, -1]

    # check for wins in the cols
    for col in range(3):
        Xcounter = 0
        Ocounter = 0
        for row in range(3):
            if board[row][col] == "X":
                Xcounter += 1
            elif board[row][col] == "O":
                Ocounter += 1
            else:
                blanks += 1
                break
        if Xcounter == 3:
            return [True, 1]
        elif Ocounter == 3:
            return [True, -1]

    # check for wins in the top left to bottom right diagonal
    Xcounter = 0
    Ocounter = 0
    for col in range(3):
        if board[col][col] == "X":
            Xcounter += 1
        elif board[col][col] == "O":
            Ocounter += 1
        else:
            blanks += 1
            break
    if Xcounter == 3:
        return [True, 1]
    elif Ocounter == 3:
        return [True, -1]

    # check for wins in the bottom left to top right diagonal
    Xcounter = 0
    Ocounter = 0
    for col in range(3):
        if board[col][2-col] == "X":
            Xcounter += 1
        elif board[col][2-col] == "O":
            Ocounter += 1
        else:
            blanks += 1
            break
    if Xcounter == 3:
        return [True, 1]
    elif Ocounter == 3:
        return [True, -1]

    if blanks == 0:
        return [True, 0]

    return [False, 0]

# takes user input and marks the space on the board. Pass in whose turn it is
def playerMove(board, symbol):
    # bulletproofing input like a responsible coder
    legalMove = False
    while not legalMove:
        moveRow = int(input("Which row? 1, 2, or 3? ")) - 1
        moveCol = int(input("Which col? 1, 2, or 3? ")) - 1
        legalMove = True
        if moveRow > 2 or moveRow < 0:
            print("Your row wasn't in the range.")
            legalMove = False
        if moveCol > 2 or moveCol < 0:
            print("Your col wasn't in the range.")
            legalMove = False
        if legalMove and board[moveRow][moveCol] != "_":
            legalMove = False
            print("That space is taken!!")

        if not legalMove:
            print()

    board[moveRow][moveCol] = symbol
    return board

# returns [row, col] of best move
# Follows these logic steps:
# 1) If it can win, it wins
# 2) If opponent is about to win, stop opponent
# 3) If it can set up two in a row, and neither of the above is possible, do it
#        - if the center is one of those, choose it!
#        - otherwise, if corners can set up, take one of those
# 4) if none of the above is possible, center > corners > other
def computerMove(board, symbol):
    saves = []
    setup = []
    other = []

    # we'll use this later
    corners = [[0, 0], [0, 2], [2, 2], [2, 0]]

    # Check the rows
    for row in range(3):
        ours = 0
        opponent = 0
        spaces = []
        for col in range(3):
            if board[row][col] == symbol:
                ours += 1
            elif board[row][col] != "_":
                opponent += 1
            else:
                spaces.append(col)

        if ours == 2 and opponent == 0:
            # if we can win, take it
            return [row, spaces[0]]

        elif ours == 0 and opponent == 2:
            # if opponent can win, add the move to saves
            saves.append([row, spaces[0]])

        elif ours == 1 and opponent == 0:
            setup.append([row, spaces[0]])

        else:
            for move in spaces:
                other.append([row, move])

        # Check the cols
        for col in range(3):
            ours = 0
            opponent = 0
            spaces = []
            for row in range(3):
                if board[row][col] == symbol:
                    ours += 1
                elif board[row][col] != "_":
                    opponent += 1
                else:
                    spaces.append(row)

            if ours == 2 and opponent == 0:
                # if we can win, take it
                return [spaces[0], col]

            elif ours == 0 and opponent == 2:
                # if opponent can win, add the move to saves
                saves.append([spaces[0], col])

            elif ours == 1 and opponent == 0:
                setup.append([spaces[0], col])

            else:
                for move in spaces:
                    other.append([move, col])

    # Check diagonal top left to bottom right
    ours = 0
    opponent = 0
    spaces = []

    for row in range(3):

        if board[row][row] == symbol:
            ours += 1
        elif board[row][row] != "_":
            opponent += 1
        else:
            spaces.append(row)

    if ours == 2 and opponent == 0:
        # if we can win, take it
        return [spaces[0], spaces[0]]

    elif ours == 0 and opponent == 2:
        # if opponent can win, add the move to saves
        saves.append([spaces[0], spaces[0]])

    elif ours == 1 and opponent == 0:
            setup.append([spaces[0], spaces[0]])

    else:
        for move in spaces:
            other.append([move, move])

    # Check diagonal bottom left to top right
    ours = 0
    opponent = 0
    spaces = []

    for row in range(3):

        if board[row][2-row] == symbol:
            ours += 1
        elif board[row][2-row] != "_":
            opponent += 1
        else:
            spaces.append(2-row)

    if ours == 2 and opponent == 0:
        # if we can win, take it
        return [2-spaces[0], spaces[0]]

    elif ours == 0 and opponent == 2:
        # if opponent can win, add the move to saves
        saves.append([2-spaces[0], spaces[0]])

    elif ours == 1 and opponent == 0:
        setup.append([2-spaces[0], spaces[0]])

    else:
        for move in spaces:
            other.append([2-move, move])


    # now that all moves have been evaluated, go down the list
    if len(saves) != 0:
        #print("SAVE")
        return saves[0]

    if len(setup) != 0:
        #print("SETUP")
        if [1, 1] in setup:
            #print("CENTER")
            return [1, 1]
        else:
            for move in corners:
                if move in setup:
                    #print("CORNER")
                    return move
        return setup[0]

    else:
        #print("RANDOM")
        if [1, 1] in other:
            #print("CENTER")
            return [1, 1]
        for move in corners:
            if move in setup:
                #print("CORNER")
                return move
        return other[0]

# This is the minimax function! It returns 1 if the board is winning, 0 if it's going to a draw, and -1
# if you will lose for sure
def scoreBoard(board, symbol):
    #print(board, symbol)
    #ready = input()
    current = gameOver(board)

    # base case!
    if current[0]:
        if current[1] == 0:
            return 0
        elif current[1] == 1:
            if symbol == "X":
                printBoard(board)
                ready = input()
                return 1
            else:
                return -1
        else:
            if symbol == "X":
                return -1
            else:
                return 1

    if symbol == "X":
        other = "O"
    else:
        other = "X"

    maxScore = -1

    for r in range(3):
        for c in range(3):
            # if it's a possible move
            if board[r][c] == "_":
                newBoard = copyBoard(board)
                newBoard[r][c] = symbol
                score = -scoreBoard(newBoard, other)
                if score > maxScore:
                    maxScore = score

    return maxScore


def gradeMove(board):
    before = -scoreBoard(board, "O")
    move = computerMove(board, "O")
    newBoard = copyBoard(board)
    newBoard[move[0]][move[1]] = "O"
    after = scoreBoard(newBoard, "X")

    if before < after:
        return False
    else:
        return True

#print(gradeMove([["X", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]))
#ready = input()

def arr_to_str(board):

    string = ""

    for row in range(3):
        for col in range(3):
            string += board[row][col]

    return string

def getAllBoards(moveDepth):
    #print(moveDepth)
    if moveDepth == 0:
        #print("bottom")
        return [[["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]]
    else:
        if moveDepth % 2 == 1:
            symbol = "X"
        else:
            symbol = "O"
        boards = getAllBoards(moveDepth-1)
        newBoards = []
        for board in boards:
            for r in range(3):
                for c in range(3):
                    newBoard = copyBoard(board)
                    if newBoard[r][c] == "_":
                        newBoard[r][c] = symbol
                        if not gameOver(newBoard)[0]:
                            newBoards.append(copyBoard(newBoard))
        return newBoards

"""print("starting")
boards = getAllBoards(1)
for board in boards:
    printBoard(board)
    print()
print("done")
ready = input()
#print("done")
"""
correct = 0
total = 0
for i in range(8):
    if i % 2 == 1:
        thisCorrect = 0
        numBoards = getAllBoards(i)
        total += len(numBoards)
        for board in numBoards:
            grade = gradeMove(board)
            if grade:
                correct += 1
                thisCorrect += 1
            #else:
                #printBoard(board)
                #print(computerMove(board, "O"))
                #ready = input()
        print("After reviewing all",i, "move boards, out of", len(numBoards), "boards logic steps got", thisCorrect, "correct")


print("TOTAL:", total)
print("PERCENTAGE CORRECT:", correct/total)
print("done")


def playGame():
    # set the turn. even is X's, odd is O's
    turn = 0

    # set the board
    board = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"]
    ]

    finished = False

    # game loop

    while not finished:
        if turn % 2 == 0:
            before = scoreBoard(board, "X")
            # X's turn
            board = playerMove(board, "X")
            after = -scoreBoard(board, "O")

            print("SCORE FOR X IS:", -scoreBoard(board, "O"))
        else:
            before = -scoreBoard(board, "O")

            #board = playerMove(board, "O")
            move = computerMove(board, "O")
            board[move[0]][move[1]] = "O"
            after = scoreBoard(board, "X")

            print("SCORE FOR X IS:", scoreBoard(board, "X"))
        if after < before:
            print("THE PLAYER MESSED UP!!!!")
        if after > before:
            print("THE COMPUTER MESSED UP!!!")


        result = gameOver(board)

        if result[0]:
            finished = True
            if result[1] == 0:
                print("It's a tie!")
            elif result[1] == 1:
                print("X WINS!")
            else:
                print("O WINS!")

        printBoard(board)
        print()
        turn += 1

#playGame()




