# Import modules
from importlib import reload
import fourbyfour as fbf
import ai_first_threebythree as ai_f
import player_first_threebythree as pl_f


menu = """
       1. 3x3 - AI plays first
       2. 3x3 - Player plays first
       3. 4x4
       Q. Quit
       """


def main():
    game_still_on = True

    while game_still_on:
        print(menu)
        player_choice = input(
            "Which version of X and O would you like to play? ")

        # Before the game starts, all the variables are set to the preferred inital values

        while player_choice not in ["1", "2", "3", "Q", "q"]:
            player_choice = input("Pick a valid option")

        if player_choice == "1":
            ai_f.game_is_still_on = True
            ai_f.moves_made = 0
            ai_f.PLAYER, ai_f.AI = 'X', 'O'
            ai_f.MAX = 1000
            ai_f.MIN = -1000
            ai_f.current_player = ai_f.PLAYER

            ai_f.board = [
                "-", "-", "-",
                "-", "-", "-",
                "-", "-", "-"
            ]

            ai_f.play_game(ai_f.board)

        elif player_choice == "2":
            pl_f.game_is_still_on = True
            pl_f.moves_made = 0
            pl_f.PLAYER, pl_f.AI = 'X', 'O'
            pl_f.MAX = 1000
            pl_f.MIN = -1000
            pl_f.current_player = pl_f.PLAYER

            pl_f.board = [
                "-", "-", "-",
                "-", "-", "-",
                "-", "-", "-"
            ]

            pl_f.play_game(pl_f.board)
        elif player_choice == "3":
            fbf.game_is_still_on = True
            fbf.moves_made = 0
            fbf.PLAYER, fbf.AI = 'X', 'O'
            fbf.MAX = 1000
            fbf.MIN = -1000
            fbf.current_player = fbf.PLAYER

            fbf.board = [
                "-", "-", "-", "-",
                "-", "-", "-", "-",
                "-", "-", "-", "-",
                "-", "-", "-", "-"
            ]

            fbf.play_game(fbf.board)
        elif player_choice == ("Q"):
            game_still_on = False
        elif player_choice == ("q"):
            game_still_on = False


main()
