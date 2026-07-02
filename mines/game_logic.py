import random
import time

class GameLogic:
    """
    Handles the core game logic for 2-Player Minesweeper.
    This layer is responsible for initializing the game, processing player inputs
    (clicks from the UI layer), and determining game state changes (win/loss).
    It acts as the intermediary between the UI and Data Management layers.
    """
    def __init__(self, data_manager, results_layer, board_size=10, num_mines=10):
        self.data_manager = data_manager
        self.results_layer = results_layer
        self.board_size = board_size
        self.num_mines = num_mines
        self.game_over = False
        self.start_time = None
        self.player_start_times = [None, None]

    def start_game(self):
        """Initializes the game for both players."""
        self.start_time = time.time()
        for player_id in range(2):
            self.data_manager.initialize_player_data(player_id, self.board_size, self.num_mines)
        # We don't place mines until the first click to ensure a safe first move.

    def on_left_click(self, player_id, row, col):
        """Handles a left-click action from a player."""
        if self.game_over or self.data_manager.is_revealed(player_id, row, col):
            return

        # Start timer on the  first click
        if self.player_start_times[player_id] is None:
            self.player_start_times[player_id] = time.time()
            # Generate board now to ensure first click is not a mine
            self.data_manager.place_mines(player_id, (row, col))
            self.data_manager.calculate_adjacent_mines(player_id)

        self.reveal_cell(player_id, row, col)

        if self.check_win_condition(player_id):
            self.game_over = True
            player_data = self.data_manager.get_player_data(player_id)
            player_data['time_elapsed'] = time.time() - self.player_start_times[player_id]
            self.results_layer.show_winner(player_id, player_data['time_elapsed'])

    def on_right_click(self, player_id, row, col):
        """Handles a right-click action (flagging) from a player."""
        if self.game_over or self.data_manager.is_revealed(player_id, row, col):
            return
        
        self.data_manager.toggle_flag(player_id, row, col)
        # The UI layer will be responsible for updating the mine count display

    def reveal_cell(self, player_id, row, col):
        """Reveals a cell and handles the consequences (mine or empty)."""
        if self.data_manager.is_mine(player_id, row, col):
            self.game_over = True
            self.data_manager.get_player_data(player_id)['time_elapsed'] = time.time() - self.player_start_times[player_id]
            self.results_layer.show_loser(player_id)
            self.data_manager.reveal_all_mines(player_id)
            return

        # Use a queue for flood fill (reveal adjacent empty cells)
        queue = [(row, col)]
        visited = set()

        while queue:
            r, c = queue.pop(0)
            if (r, c) in visited or not self.data_manager.is_valid_cell(player_id, r, c):
                continue
            
            visited.add((r, c))
            self.data_manager.reveal_cell(player_id, r, c)

            if self.data_manager.get_cell_data(player_id, r, c)['adjacent_mines'] == 0:
                # If the cell is empty, reveal its neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if (nr, nc) not in visited:
                            queue.append((nr, nc))
    
    def check_win_condition(self, player_id):
        """Checks if a player has won the game."""
        player_data = self.data_manager.get_player_data(player_id)
        revealed_count = 0
        for r in range(self.board_size):
            for c in range(self.board_size):
                if player_data['board'][r][c]['is_revealed']:
                    revealed_count += 1
        
        # Win if all non-mine cells are revealed
        return revealed_count == (self.board_size * self.board_size - self.num_mines)

    def update_game_time(self):
        """Updates the elapsed time for each active player."""
        for player_id in range(2):
            if self.player_start_times[player_id] is not None and not self.game_over:
                self.data_manager.get_player_data(player_id)['time_elapsed'] = time.time() - self.player_start_times[player_id]
