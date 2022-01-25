# 4X4 One Last Try

# --- Global Variables ---
from random import randrange


game_is_still_on = True
moves_made = 0

# --- Constants ---
PLAYER, AI = 'X', 'O'
MAX = 1000
MIN = -1000

# who won?
# winner = None

# who's turn is it
current_player = PLAYER

board = [
         "-", "-", "-", "-",
         "-", "-", "-", "-",
         "-", "-", "-", "-",
         "-", "-", "-", "-"
]


def show_board(board):
    """
    Displays the board in a 4x4 grid
    """
    print(board[0] + " | " + board[1] + " | " + board[2] + " | " + board[3])
    print(board[4] + " | " + board[5] + " | " + board[6] + " | " + board[7])
    print(board[8] + " | " + board[9] + " | " + board[10] + " | " + board[11])
    print(board[12] + " | " + board[13] +
          " | " + board[14] + " | " + board[15])


def check_if_game_over(board, is_evaluating):
    """
    Checks if a player has won\n
    or\n
    If the game is a tie
    """
    check_win(board, is_evaluating)
    check_tie(board)


def check_win(board, is_evaluating) -> str:
    """
    Checks win across rows, columns and diagonals.\n
    Returns the player that won: X or O
    """

    # check_rows()
    row_winner = check_rows(board, is_evaluating)

    # check_columns()
    column_winner = check_columns(board, is_evaluating)

    # check_diagonals()
    diagonals_winner = check_diagonals(board, is_evaluating)

    if row_winner:
        winner = row_winner
        return winner

    elif column_winner:
        winner = column_winner
        return winner

    elif diagonals_winner:
        winner = diagonals_winner
        return winner
    else:
        winner = None
        return winner


def check_rows(board, is_evaluating) -> str:
    """
    Checks if the game has been won on a row\n
    Returns the opponent that won
    """
    global game_is_still_on

    # check if any rows sum up to a winning value
    row_1 = board[0] == board[1] == board[2] == board[3] != "-"
    row_2 = board[4] == board[5] == board[6] == board[7] != "-"
    row_3 = board[8] == board[9] == board[10] == board[11] != "-"
    row_4 = board[12] == board[13] == board[14] == board[15] != "-"

    if (row_1 or row_2 or row_3 or row_4) and (is_evaluating == False):
        game_is_still_on = False

    # returns the winner
    if row_1:
        return board[0]
    elif row_2:
        return board[4]
    elif row_3:
        return board[8]
    elif row_4:
        return board[12]


def check_columns(board, is_evaluating) -> str:
    """
    Checks if the game has been won on a column\n
    Returns the opponent that won
    """
    global game_is_still_on

    # check if any columns sum up to a winning value
    column_1 = board[0] == board[4] == board[8] == board[12] != "-"
    column_2 = board[1] == board[5] == board[9] == board[13] != "-"
    column_3 = board[2] == board[6] == board[10] == board[14] != "-"
    column_4 = board[3] == board[7] == board[11] == board[15] != "-"

    if(column_1 or column_2 or column_3 or column_4) and (is_evaluating == False):
        game_is_still_on = False

    # returns the winner
    if column_1:
        return board[0]
    elif column_2:
        return board[1]
    elif column_3:
        return board[2]
    elif column_4:
        return board[3]


def check_diagonals(board, is_evaluating) -> str:
    """
    Checks if the game has been won on a diagonal\n
    Returns the opponent that won
    """
    global game_is_still_on

    # check if any diagonals sum up to a winning value
    diagonal_1 = board[0] == board[5] == board[10] == board[15] != "-"
    diagonal_2 = board[3] == board[6] == board[9] == board[12] != "-"

    if (diagonal_1 or diagonal_2) and (is_evaluating == False):
        game_is_still_on = False

    # returns the winner
    if diagonal_1:
        return board[0]
    elif diagonal_2:
        return board[3]


def check_tie(board):
    """
    Checks if the game ended as a draw\n
    Changes the game_is_still_on variable and ends the game
    """
    global game_is_still_on

    if "-" not in board:
        game_is_still_on = False


def flip_player():
    '''
    Switches players after a turn
    '''

    global current_player

    if current_player == PLAYER:
        current_player = AI
    elif current_player == AI:
        current_player = PLAYER


def handle_turn(player, board):
    if player == "X":
        print(player + "'s turn.")
        position = input("Choose a number from 1-16: ")
        valid_move = False

        # prevents one player from over-writing his opponent's move
        while not valid_move:

            # limits selection to the grid
            while position not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"]:
                position = input("Invalid input. Choose a number from 1-16: ")

            # index is 0-15, not 1-16
            position = int(position) - 1

            # one can only play in an empty spot
            if board[position] == "-":
                valid_move = True
                board[position] = player  # easiest bug fix of my life
            else:
                print("You can't play there. Go again.")

    elif player == "O":
        print(player + "'s turn.")

        if moves_made >= 5:  # it takes 5 moves to set up a win
            # plays the best move for the board state
            position = find_best_move(board)
        else:
            position = return_random_move(board)
        board[position] = player

    show_board(board)


def isMovesLeft(board):
    for i in range(16):
        if (board[i] == '-'):
            return True
    return False


def return_random_move(board):
    """
    Picks a random move from the board
    """
    valid_move = False

    while not valid_move:
        # index of board is 0-15
        position = randrange(0, 15)

        if board[position] == "-":
            valid_move = True
        else:
            position = randrange(0, 15)

    return position


def evaluate(board):
    """
    Evaluates the board state and returns the score
    """
    if check_win(board, True) == "X":
        return -10
    if check_win(board, True) == "O":
        return 10
    return 0   


def find_best_move(board):
    bestVal = MIN
    bestMove = -1

    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for i in range(16):

        # Check if cell is empty
        if (board[i] == '-'):

            # Make the move
            board[i] = AI

            # compute evaluation function for this
            # move.
            moveVal = minimax(board, 0, False, MIN, MAX)

            # Undo the move
            board[i] = '-'

            # If the value of the current move is
            # more than the best value, then update
            # best/
            if (moveVal > bestVal):
                bestMove = i
                bestVal = moveVal

    print("The value of the best Move is :", bestVal)
    print(bestMove)
    return bestMove


def minimax(board, depth, is_max, alpha, beta):
    score = evaluate(board)

    # If Maximizer has won the game return his/her
    # evaluated score
    if (score == 10):
        return score

    # If Minimizer has won the game return his/her
    # evaluated score
    if (score == -10):
        return score

    # If there are no more moves and no winner then
    # it is a tie
    if (isMovesLeft(board) == False):
        return 0

    scores = []

    # If this maximizer's move
    if (is_max):
        best = MIN

        # Traverse all cells
        for i in range(16):
            # Check if cell is empty
            if (board[i] == '-'):

                # Make the move
                board[i] = AI

                # Call minimax recursively and choose
                # the maximum value
                best_val = minimax(board,
                                   depth + 1,
                                   not is_max, alpha, beta)

                scores.append(best_val)

                best = max(best, max(scores))
                alpha = max(alpha, best)

                # Undo the move
                board[i] = '-'

                if beta <= alpha:
                    break
        return best

    # If this minimizer's move
    else:
        best = MAX

        # Traverse all cells
        for i in range(16):

            # Check if cell is empty
            if (board[i] == '-'):

                # Make the move
                board[i] = PLAYER

                # Call minimax recursively and choose
                # the minimum value
                best_val = minimax(board, depth + 1, not is_max, alpha, beta)

                scores.append(best_val)

                best = min(best, min(scores))
                beta = min(beta, best)

                # Undo the move
                board[i] = '-'

                if beta <= alpha:
                    break
        return best


def play_game(board):
    global moves_made
    show_board(board)

    while game_is_still_on:
        handle_turn(current_player, board)
        moves_made += 1

        # check if game is over after 7 moves
        if moves_made >= 7:
            check_if_game_over(board, False)

        # give the other player a chance
        flip_player()

    winner = check_win(board, False)

    # game is over
    if winner == "X" or winner == "O":
        print(winner + " won!")
    elif winner == None:
        print("Draw...")


play_game(board)
