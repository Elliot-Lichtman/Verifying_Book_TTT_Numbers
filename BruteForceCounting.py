
######################
# FUNCTION DEFINITIONS
######################

def is_game_over(board):

    # check for 3 in a rows 
    ########################

    # horizontal
    for row in range(3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2] and board[row][0] != "_":
            return True

    # vertical
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col] and board[0][col] != "_":
            return True
    
    # diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != "_":
        return True
    
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != "_":
        return True
    
    ##########################

    # if no 3 in a row, check for all spaces filled up (draw)

    # if there's a blank space, return that the game is not over
    for row in range(3):
        for col in range(3):
            if board[row][col] == "_":
                return False
    
    # otherwise, the game is over
    return True

# Generates all possible next boards
def get_next_boards(board, turn):
    next_boards = []

    # find all empty spaces
    for row in range(3):
        for col in range(3):
            if board[row][col] == "_":

                # copy the board
                new_board = copy_board(board)

                # put in the symbol
                new_board[row][col] = turn

                # add it to next_boards
                next_boards.append(new_board)
    
    return next_boards

# for debug code
def print_board(board):
    for row in range(3):
        for col in range(3):
            print(board[row][col], end = " ")
        print()

# Converts the array to a string (so that it can be put into a dictionary hash function)
# The rational here is that dictionaries can't store complex things like arrays 
# because there is no built in hash functions for arrays. There is one for strings though.
# Just need to make sure the string is unique for each board
def arr_to_str(board):

    string = ""

    for row in range(3):
        for col in range(3):
            string += board[row][col]

    return string

# Do I need to eplain these ones... :)

def copy_list(list):
    new_list = []
    
    for item in list:
        new_list.append(item)
    
    return new_list

def copy_board(board):
    
    new_board = []

    for row in board:
        new_board.append(copy_list(row))

    return new_board



##################
# MAIN PROGRAM
##################


# create an empty dict of boards
board_dict = {}

# I'm going to approach this with a BFS starting from an empty board

# create an empty board and add it to the dictionary
empty_board = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
# put in a placeholder in the dictionary
board_dict[arr_to_str(empty_board)] = 0

# create the BFS queue
queue = [empty_board]

# keep track of whose turn it is 
current_player = "X"

# continue until the queue is empty
while not len(queue) == 0:

    # create a replacement queue
    next_queue = []

    # for every board in the queue, expand one step
    for board in queue:

        # if the board isn't dead, get next steps
        if not is_game_over(board):
        
            # go through the board and replace every blank with current_player
            next_boards = get_next_boards(board, current_player)

            for next_board in next_boards:
                next_queue.append(next_board)
                board_dict[arr_to_str(next_board)] = 0

    queue = next_queue
    
    # change the turn
    if current_player == "X":
        current_player = "O"
    
    else:
        current_player = "X"

print(len(board_dict))

