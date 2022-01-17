from shutil import move
import numpy as np

# --- Global Variables ---
game_is_still_on = True
moves_made = 0

# who won?
winner = None

# who's turn is it
current_player = "X"

# Game board
board = [
    "-", "-", "-", "-",
         "-", "-", "-", "-",
         "-", "-", "-", "-",
         "-", "-", "-", "-"
]


def show_board():
    print(board[0] + " | " + board[1] + " | " + board[2] + " | " + board[3])
    print(board[4] + " | " + board[5] + " | " + board[6] + " | " + board[7])
    print(board[8] + " | " + board[9] + " | " + board[10] + " | " + board[11])
    print(board[12] + " | " + board[13] +
          " | " + board[14] + " | " + board[15])

# needs board, current player, no of moves


def play_game():
    global moves_made
    show_board()

    while game_is_still_on:
        handle_turn(current_player)

        # check if game is over after 7 moves
        if moves_made >= 7:
            check_if_game_over()

        # give the other player a chance
        flip_player()
        moves_made += 1

    # game is over
    if winner == "X" or winner == "O":
        print(winner + " won!")
    elif winner == None:
        print("Draw...")


def check_if_game_over():
    check_win()
    check_tie()


def check_win():
    # set global variables
    global winner

    # check_rows()
    row_winner = check_rows()

    # check_columns()
    column_winner = check_columns()

    # check_diagonals()
    diagonals_winner = check_diagonals()

    if row_winner:
        winner = row_winner

    elif column_winner:
        winner = column_winner

    elif diagonals_winner:
        winner = diagonals_winner
    else:
        winner = None

    return


def check_rows():
    global game_is_still_on

    # check if any rows sum up to a winning value
    row_1 = board[0] == board[1] == board[2] == board[3] != "-"
    row_2 = board[4] == board[5] == board[6] == board[7] != "-"
    row_3 = board[8] == board[9] == board[10] == board[11] != "-"
    row_4 = board[12] == board[13] == board[14] == board[15] != "-"

    if row_1 or row_2 or row_3 or row_4:
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
    return


def check_columns():
    global game_is_still_on

    # check if any columns sum up to a winning value
    column_1 = board[0] == board[4] == board[8] == board[12] != "-"
    column_2 = board[1] == board[5] == board[9] == board[13] != "-"
    column_3 = board[2] == board[6] == board[10] == board[14] != "-"
    column_4 = board[3] == board[7] == board[11] == board[15] != "-"

    if column_1 or column_2 or column_3 or column_4:
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
    return


def check_diagonals():
    global game_is_still_on

    # check if any diagonals sum up to a winning value
    diagonal_1 = board[0] == board[5] == board[10] == board[15] != "-"
    diagonal_2 = board[3] == board[6] == board[9] == board[12] != "-"

    if diagonal_1 or diagonal_2:
        game_is_still_on = False

    # returns the winner
    if diagonal_1:
        return board[0]
    elif diagonal_2:
        return board[3]
    return


def check_tie():
    global game_is_still_on

    if "-" not in board:
        game_is_still_on = False
    return


def flip_player():
    # switches players after a turn
    global current_player

    if current_player == "X":
        current_player = "O"
    elif current_player == "O":
        current_player = "X"
    return


def handle_turn(player):

    print(player + "'s turn.")
    position = input("Choose a number from 1-16: ")
    valid_move = False

    while not valid_move:

        while position not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"]:
            position = input("Invalid input. Choose a number from 1-16: ")

        position = int(position) - 1

        if board[position] == "-":
            valid_move = True
        else:
            print("You can't play there. Go again.")

    board[position] = player
    show_board()


play_game()