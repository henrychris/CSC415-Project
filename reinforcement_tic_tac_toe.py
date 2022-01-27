import gym
import random
import numpy

# AI GOES FIRST

# --- Global Variables ---
game_is_still_on = True
moves_made = 0
p1_states_value = {}
p1_states = []
lr = 0.2
decay_gamma = 0.9
exp_rate = 0.3
p1_reward = 0
p2_reward = 0

# --- Constants ---
PLAYER, AI = 'X', 'O'
MAX = 1000
MIN = -1000

# who won?
# winner = None

# who's turn is it
current_player = PLAYER

board = [
    "-", "-", "-",
    "-", "-", "-",
    "-", "-", "-"
]


def show_board(board):
    """
    Displays the board in a 3x3 grid
    """
    print(board[0] + " | " + board[1] + " | " + board[2])
    print(board[3] + " | " + board[4] + " | " + board[5])
    print(board[6] + " | " + board[7] + " | " + board[8])


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


def check_rows(board, is_evaluating):
    """
    Checks if the game has been won on a row\n
    Returns the opponent that won
    """
    global game_is_still_on

    # check if any rows sum up to a winning value
    row_1 = board[0] == board[1] == board[2] != "-"
    row_2 = board[3] == board[4] == board[5] != "-"
    row_3 = board[6] == board[7] == board[8] != "-"

    if (row_1 or row_2 or row_3) and (is_evaluating == False):
        # is_evaluating should prevent the game from ending early
        game_is_still_on = False

    # returns the winner
    if row_1:
        return board[0]
    elif row_2:
        return board[3]
    elif row_3:
        return board[6]


def check_columns(board, is_evaluating):
    """
    Checks if the game has been won on a column\n
    Returns the opponent that won
    """
    global game_is_still_on

    # check if any columns sum up to a winning value
    column_1 = board[0] == board[3] == board[6] != "-"
    column_2 = board[1] == board[4] == board[7] != "-"
    column_3 = board[2] == board[5] == board[8] != "-"

    if (column_1 or column_2 or column_3) and (is_evaluating == False):
        game_is_still_on = False

    # returns the winner
    if column_1:
        return board[0]
    elif column_2:
        return board[1]
    elif column_3:
        return board[2]


def check_diagonals(board, is_evaluating) -> str:
    """
    Checks if the game has been won on a diagonal\n
    Returns the opponent that won
    """
    global game_is_still_on

    # check if any diagonals sum up to a winning value
    diagonal_1 = board[0] == board[4] == board[8] != "-"
    diagonal_2 = board[2] == board[4] == board[6] != "-"

    if (diagonal_1 or diagonal_2) and (is_evaluating == False):
        game_is_still_on = False

    # returns the winner
    if diagonal_1:
        return board[0]
    elif diagonal_2:
        return board[2]


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

def return_random_move(board):
    """
    Picks a random move from the board
    """
    valid_move = False

    while not valid_move:
        position = random.randrange(0,9)

        if board[position] == "-":
            valid_move = True
        else:
            position = random.randrange(0, 9)

    return position

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
        for i in range(9):
            # Check if cell is empty
            if (board[i] == '-'):

                # Make the move
                board[i] = PLAYER

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
        for i in range(9):

            # Check if cell is empty
            if (board[i] == '-'):

                # Make the move
                board[i] = AI

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

def find_best_move(board):
    bestVal = MIN
    bestMove = -1

    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for i in range(9):

        # Check if cell is empty
        if (board[i] == '-'):

            # Make the move
            board[i] = PLAYER

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

    # print("The value of the best Move is :", bestVal)
    # print(bestMove)
    return bestMove


def board_hash(board):
    return str(board)

def choose_action(board, available_positions, exp_rate, symbol, states_value):
    position = -1
    if(numpy.random.uniform(0,1)) <= exp_rate:
        index = numpy.random.choice(len(available_positions))
        # position = return_random_move(board)
        position = available_positions[index]
    else:
        value_max = -999
        for p in available_positions:
            next_board = board.copy()
            next_board[p] = symbol
            next_board_hash = board_hash(next_board)
            value = 0 if states_value.get(next_board_hash) is None else states_value.get(next_board_hash)
            if value >= value_max:
                value_max = value
                position = p
    return position

def add_state(states, state):
    states.append(state)

def feed_reward(reward, states, states_value):
    for state in reversed(states):
        if states_value.get(state) is None:
            states_value[state] = 0
        states_value[state] += lr * (decay_gamma * reward - states_value[state])
        reward = states_value[state]

def find_available_positions(board):
    positions = []
    for position in range(len(board)):
        if board[position] == '-':
            positions.append(position)
    return positions

def give_reward(winner):
    if winner == 'X':
        feed_reward(1, p1_states, p1_states_value)
    elif winner == 'O':
        feed_reward(0, p1_states, p1_states_value)
    else:
        feed_reward(0.1, p1_states, p1_states_value)

def isMovesLeft(board):

    for i in range(9):
        if (board[i] == '-'):
            return True
    return False


def evaluate(board):
    """
    Evaluates the board state and returns the score
    """
    if check_rows(board, True) == "X":
        return 10
    if check_rows(board, True) == "O":
        return -10
    if check_columns(board, True) == "X":
        return 10
    if check_columns(board, True) == "O":
        return -10
    if check_diagonals(board, True) == "X":
        return 10
    if check_diagonals(board, True) == "O":
        return -10
    return 0


def play_game(board):
    global moves_made
    global game_is_still_on

    # show_board(board)

    while game_is_still_on:
        # handle_turn(current_player, board)
        if current_player == PLAYER:
            position = choose_action(board, find_available_positions(board), exp_rate, current_player, p1_states_value)
            board[position] = current_player
            add_state(p1_states, board_hash(board))
        else:
            position = find_best_move(board)
            board[position] = current_player
        moves_made += 1
        # check if game is over after 7 moves
        if moves_made >= 5:
            check_if_game_over(board, False)

        # give the other player a chance
        flip_player()

    winner = check_win(board, False)
    show_board(board)
    # game is over
    if winner == "X" or winner == "O":
        print(winner + " won!")
    elif winner == None:
        print("Draw...")
    give_reward(winner)
    reset()

def play_game_2(board):
    global moves_made
    global game_is_still_on

    # show_board(board)

    while game_is_still_on:
        # handle_turn(current_player, board)
        if current_player == PLAYER:
            
            position = input("Choose a number from 1-9: ")
            valid_move = False

            # prevents one player from over-writing his opponent's move
            while not valid_move:

            # limits selection to the grid
                while position not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    position = input("Invalid input. Choose a number from 1-9: ")

                # index is 0-9
                position = int(position) - 1

                # one can only play in an empty spot
                if board[position] == "-":
                    valid_move = True
                    board[position] = current_player  # easiest bug fix of my life
                else:
                    print("You can't play there. Go again.")
        else:
            position = choose_action(board, find_available_positions(board), exp_rate, current_player, p1_states_value)
            board[position] = current_player
            add_state(p1_states, board_hash(board))
        moves_made += 1
        # check if game is over after 7 moves
        if moves_made >= 5:
            check_if_game_over(board, False)

        # give the other player a chance
        flip_player()
        show_board(board)

    winner = check_win(board, False)
    show_board(board)
    # game is over
    if winner == "X" or winner == "O":
        print(winner + " won!")
    elif winner == None:
        print("Draw...")
    give_reward(winner)
    reset()

def reset():
    global game_is_still_on
    global moves_made
    global current_player
    game_is_still_on = True
    moves_made = 0
    current_player = PLAYER
    board.clear()
    for i in range(9):
        board.append('-')
    p1_states.clear()

# show_board(board)
for i in range(100):
    play_game(board)
print(str(p1_states_value))
play_game_2(board)