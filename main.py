# Import modules
import fourbyfour as fbf
import ai_first_threebythree as ai_f
import player_first_threebythree as pl_f


# --- Global Variables ---

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

        while player_choice not in ["1", "2", "3", "Q", "q"]:
            player_choice = input("Pick a valid option")

        if player_choice == "1":
            ai_f.play_game(ai_f.board)
        elif player_choice == "2":
            pl_f.play_game(pl_f.board)
        elif player_choice == "3":
            fbf.play_game(fbf.board)
        elif player_choice == ("Q" or "q"):
            game_still_on = False


main()
