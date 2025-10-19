import random

class DataManager:
    """
    manages all game data and state for both players.
    this layer is responsible for creating and storing the game boards,
    mine locations, cell states (revealed, flagged), and player-specific
    information like timers and flag counts. It ensures data integrity
    and separation between players.
    """
    def __init__(self):
        self.players_data = {}

    def initialize_player_data(self, player_id, board_size, num_mines):
        """sets up the initial data structure for a player."""
        board = [[{
            'is_mine': False,
            'is_revealed': False,
            'is_flagged': False,
            'adjacent_mines': 0
        } for _ in range(board_size)] for _ in range(board_size)]

        self.players_data[player_id] = {
            'board': board,
            'board_size': board_size,
            'num_mines': num_mines,
            'mine_locations': set(),
            'flags_placed': 0,
            'time_elapsed': 0
        }

    def place_mines(self, player_id, first_click_pos):
        """randomly places mines on a player's board, avoiding the first click."""
        data = self.players_data[player_id]
        mines_placed = 0
        while mines_placed < data['num_mines']:
            row = random.randint(0, data['board_size'] - 1)
            col = random.randint(0, data['board_size'] - 1)
            # ensure the mine is not placed on the first clicked cell or where a mine already exists
            if (row, col) != first_click_pos and not data['board'][row][col]['is_mine']:
                data['board'][row][col]['is_mine'] = True
                data['mine_locations'].add((row, col))
                mines_placed += 1
    
    def calculate_adjacent_mines(self, player_id):
        """calculates the number of adjacent mines for each cell on the board."""
        data = self.players_data[player_id]
        for r in range(data['board_size']):
            for c in range(data['board_size']):
                if data['board'][r][c]['is_mine']:
                    continue
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if self.is_valid_cell(player_id, nr, nc) and data['board'][nr][nc]['is_mine']:
                            count += 1
                data['board'][r][c]['adjacent_mines'] = count

    def get_player_data(self, player_id):
        return self.players_data[player_id]

    def get_cell_data(self, player_id, row, col):
        return self.players_data[player_id]['board'][row][col]

    def is_valid_cell(self, player_id, row, col):
        size = self.players_data[player_id]['board_size']
        return 0 <= row < size and 0 <= col < size
        
    def is_mine(self, player_id, row, col):
        return self.get_cell_data(player_id, row, col)['is_mine']

    def is_revealed(self, player_id, row, col):
        return self.get_cell_data(player_id, row, col)['is_revealed']

    def reveal_cell(self, player_id, row, col):
        self.players_data[player_id]['board'][row][col]['is_revealed'] = True

    def toggle_flag(self, player_id, row, col):
        cell = self.get_cell_data(player_id, row, col)
        if not cell['is_flagged']:
            cell['is_flagged'] = True
            self.players_data[player_id]['flags_placed'] += 1
        else:
            cell['is_flagged'] = False
            self.players_data[player_id]['flags_placed'] -= 1

    def reveal_all_mines(self, player_id):
        """Reveals all mines for a player, usually at the end of the game."""
        data = self.players_data[player_id]
        for r, c in data['mine_locations']:
            data['board'][r][c]['is_revealed'] = True