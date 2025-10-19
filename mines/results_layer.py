import tkinter as tk
from tkinter import messagebox
import sys
import os

class ResultsLayer:
    """
    Handles the output and results of the game.
    This layer is responsible for displaying the final outcome, such as
    the winner or loser, showing final times, and providing options to
    play again or exit the application. It is triggered by the Game Logic Layer
    when a game-ending condition is met.
    """
    def __init__(self, root, ui_callback_update):
        self.root = root
        self.ui_callback_update = ui_callback_update

    def show_winner(self, player_id, time_taken):
        """Displays a message for the winning player."""
        self.reveal_all_boards()
        message = f"Player {player_id + 1} Wins!\nTime: {time_taken:.2f} seconds"
        self._show_end_dialog("Congratulations!", message)

    def show_loser(self, player_id):
        """Displays a message when a player hits a mine."""
        # The winner is the other player
        winner_id = 1 - player_id
        self.reveal_all_boards()
        message = f"Player {player_id + 1} hit a mine!\nPlayer {winner_id + 1} is the winner!"
        self._show_end_dialog("Game Over!", message)
        
    def reveal_all_boards(self):
        """Forces the UI to update all cells on both boards at game end."""
        self.ui_callback_update()

    def _show_end_dialog(self, title, message):
        """Creates the pop-up dialog for the end of the game."""
        answer = messagebox.askyesno(title, f"{message}\n\nDo you want to play again?")
        if answer:
            # Relaunch the application
            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            self.root.destroy()
