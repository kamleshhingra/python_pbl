import tkinter as tk
from ui_layer import MinesweeperGUI
from game_logic import GameLogic
from data_manager import DataManager
from results_layer import ResultsLayer

# --- Game Configuration ---
BOARD_SIZE = 10
NUM_MINES = 10

class MainApplication:
    """
    The main application class that orchestrates the different layers
    of the 2-Player Minesweeper game.
    """
    def __init__(self, root):
        self.root = root
        
        # 1. Initialize Layers
        self.data_manager = DataManager()
        self.results_layer = ResultsLayer(self.root, self.force_ui_update)
        self.game_logic = GameLogic(self.data_manager, self.results_layer, BOARD_SIZE, NUM_MINES)

        # 2. Start the Game Logic to initialize data BEFORE creating the GUI
        self.game_logic.start_game()
        
        # 3. Initialize the GUI which depends on the initialized data
        self.gui = MinesweeperGUI(self.root, self.game_logic, BOARD_SIZE, NUM_MINES)

        # 4. Connect Layers
        # The ResultsLayer needs a way to tell the UI to update all boards at the end.
        self.results_layer.ui_callback_update = self.force_ui_update

        # The game start is now called before the GUI is created, so we remove the call from here.

    def force_ui_update(self):
        """
        A callback function that iterates through every cell of both boards
        and tells the UI to update its appearance based on the final data.
        This is used by the ResultsLayer at the end of the game.
        """
        for player_id in range(2):
            player_data = self.data_manager.get_player_data(player_id)
            for r in range(player_data['board_size']):
                for c in range(player_data['board_size']):
                    cell_data = self.data_manager.get_cell_data(player_id, r, c)
                    self.gui.update_board(player_id, r, c, cell_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

