import tkinter as tk
from tkinter import messagebox

class MinesweeperGUI:
    """
    Handles the User Interface (UI) for the 2-Player Minesweeper game.
    This layer is responsible for creating the game window, drawing the grids,
    displaying timers and mine counts, and handling all user input (clicks).
    It communicates player actions to the Game Logic Layer.
    """
    def __init__(self, root, game_logic, board_size=10, num_mines=10):
        self.root = root
        self.game_logic = game_logic
        self.board_size = board_size
        self.num_mines = num_mines
        self.buttons = [{}, {}] # Buttons for Player 1 and Player 2
        self.root.title("2-Player Minesweeper")
        self.root.configure(bg='#2c3e50')

        # Main frame
        main_frame = tk.Frame(root, bg='#2c3e50', padx=10, pady=10)
        main_frame.pack()
        
        # --- Player 1 UI ---
        p1_frame = tk.Frame(main_frame, bg='#34495e', padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        p1_frame.pack(side=tk.LEFT, padx=20, pady=10)

        p1_header_frame = tk.Frame(p1_frame, bg='#34495e')
        p1_header_frame.pack(pady=(0, 10))
        
        tk.Label(p1_header_frame, text="Player 1", font=("Helvetica", 16, "bold"), fg='#ecf0f1', bg='#34495e').pack(side=tk.LEFT, padx=10)
        
        self.p1_timer_label = tk.Label(p1_header_frame, text="Time: 0s", font=("Helvetica", 12), fg='#ecf0f1', bg='#34495e')
        self.p1_timer_label.pack(side=tk.LEFT, padx=10)
        
        self.p1_mines_label = tk.Label(p1_header_frame, text=f"Mines: {num_mines}", font=("Helvetica", 12), fg='#ecf0f1', bg='#34495e')
        self.p1_mines_label.pack(side=tk.LEFT, padx=10)

        self.p1_grid_frame = tk.Frame(p1_frame, bg='#2c3e50')
        self.p1_grid_frame.pack()
        self.create_grid(0, self.p1_grid_frame)

        # --- Player 2 UI ---
        p2_frame = tk.Frame(main_frame, bg='#34495e', padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        p2_frame.pack(side=tk.RIGHT, padx=20, pady=10)

        p2_header_frame = tk.Frame(p2_frame, bg='#34495e')
        p2_header_frame.pack(pady=(0, 10))

        tk.Label(p2_header_frame, text="Player 2", font=("Helvetica", 16, "bold"), fg='#ecf0f1', bg='#34495e').pack(side=tk.LEFT, padx=10)

        self.p2_timer_label = tk.Label(p2_header_frame, text="Time: 0s", font=("Helvetica", 12), fg='#ecf0f1', bg='#34495e')
        self.p2_timer_label.pack(side=tk.LEFT, padx=10)

        self.p2_mines_label = tk.Label(p2_header_frame, text=f"Mines: {num_mines}", font=("Helvetica", 12), fg='#ecf0f1', bg='#34495e')
        self.p2_mines_label.pack(side=tk.LEFT, padx=10)

        self.p2_grid_frame = tk.Frame(p2_frame, bg='#2c3e50')
        self.p2_grid_frame.pack()
        self.create_grid(1, self.p2_grid_frame)

        self.update_timers()

    def create_grid(self, player_id, frame):
        """Creates the button grid for a given player."""
        for r in range(self.board_size):
            for c in range(self.board_size):
                button = tk.Button(frame, width=3, height=1, bg='#bdc3c7', activebackground='#e0e0e0', relief=tk.RAISED, font=('Helvetica', 10, 'bold'))
                button.grid(row=r, column=c)
                # Bind left-click to reveal and right-click to flag
                button.bind('<Button-1>', lambda e, p=player_id, r=r, c=c: self.game_logic.on_left_click(p, r, c))
                button.bind('<Button-3>', lambda e, p=player_id, r=r, c=c: self.game_logic.on_right_click(p, r, c))
                self.buttons[player_id][(r, c)] = button

    def update_board(self, player_id, row, col, cell_data):
        """Updates a single button on the grid based on game state."""
        button = self.buttons[player_id][(row, col)]
        if cell_data['is_flagged']:
            button.config(text="🚩", state=tk.DISABLED, disabledforeground='#000000', bg='#f1c40f')
        elif cell_data['is_revealed']:
            button.config(relief=tk.SUNKEN, bg='#d5dbdb', state=tk.DISABLED)
            if cell_data['is_mine']:
                button.config(text="💣", bg='#c0392b')
            elif cell_data['adjacent_mines'] > 0:
                # Color code numbers for better visibility
                colors = ['#2980b9', '#27ae60', '#d35400', '#c0392b', '#8e44ad', '#2c3e50', '#f39c12', '#7f8c8d']
                button.config(text=str(cell_data['adjacent_mines']), disabledforeground=colors[cell_data['adjacent_mines']-1])
            else:
                button.config(text="") # Empty revealed cell
        else: # Not revealed, not flagged
            button.config(text="", state=tk.NORMAL, bg='#bdc3c7')
    
    def update_timers(self):
        """Periodically updates the timer labels for both players."""
        self.game_logic.update_game_time()
        p1_time = self.game_logic.data_manager.get_player_data(0)['time_elapsed']
        p2_time = self.game_logic.data_manager.get_player_data(1)['time_elapsed']
        self.p1_timer_label.config(text=f"Time: {int(p1_time)}s")
        self.p2_timer_label.config(text=f"Time: {int(p2_time)}s")
        self.root.after(1000, self.update_timers)

    def update_mine_counts(self):
        """Updates the mine count labels based on flags placed."""
        p1_flags = self.game_logic.data_manager.get_player_data(0)['flags_placed']
        p2_flags = self.game_logic.data_manager.get_player_data(1)['flags_placed']
        self.p1_mines_label.config(text=f"Mines: {self.num_mines - p1_flags}")
        self.p2_mines_label.config(text=f"Mines: {self.num_mines - p2_flags}")