class Engine:
    def __init__(self):
        # fmt: off
        self.board = ["r","n","b","q","k","b","n","r",
                     "p","p","p","p","p","p","p","p",
                     ".",".",".",".",".",".",".",".",
                     ".",".",".",".",".",".",".",".",
                     ".",".",".",".",".",".",".",".",
                     ".",".",".",".",".",".",".",".",
                     "P","P","P","P","P","P","P","P",
                     "R","N","B","Q","K","B","N","R"]
        # fmt: on
        self.delta_pos = {"first_click": "", "second_click": ""}
        self.valid_moves = []
        self.first_selection = None  # TODO: try to make selection vars local
        self.second_selection = None

    def get_piece(self, index):
        return self.board[index]

    def get_index_from_position(self, click_pos):
        selected_row = click_pos[1] // 100
        selected_col = click_pos[0] // 100
        # NOT DYNAMIC don't change the board size #TODO: get the click position dynamiclly
        index = (selected_row * 8) + selected_col
        self.get_selections(index)

    def get_selections(self, index):
        if self.first_selection == None:
            if self.board[index] != ".":
                self.first_selection = index
                self.get_valid_moves(self.first_selection)
                print(self.valid_moves)
                # highlight_valid_moves(self.valid_moves)
        else:
            self.second_selection = index
            self.is_same_color()

    def is_same_color(self):
        if self.board[self.second_selection].isalpha():
            if (
                self.board[self.first_selection].isupper()
                == self.board[self.second_selection].isupper()
            ):
                self.first_selection = self.second_selection
                self.second_selection = None
                self.get_valid_moves(self.first_selection)
                print(self.valid_moves)
                # highlight_valid_moves(self.valid_moves)
        self.move_pieces()

    def move_pieces(self):
        if self.second_selection in self.valid_moves:
            self.board[self.second_selection] = self.board[self.first_selection]
            self.board[self.first_selection] = "."
            self.clear_values()

    def clear_values(self):
        self.first_selection = None
        self.second_selection = None
        self.valid_moves = []

    def get_valid_moves(self, index):  # TODO: turn index to row and col
        self.valid_moves = []
        piece_movements = {
            "rook": [8, -8, 1, -1],
            "bishop": [9, -9, 7, -7],
            "queen": [8, -8, 1, -1, 9, -9, 7, -7],
        }

        if self.board[index] == "P":
            if index // 8 == 6:
                if self.board[index - 16] == ".":
                    self.valid_moves.append(index - 16)
            if self.board[index - 8] == ".":
                self.valid_moves.append(index - 8)
            if self.board[index - 7] != ".":  # BUG: edge case index 55, 8
                self.valid_moves.append(index - 7)
            if self.board[index - 9] != ".":  # BUG: edge case index 48, 15
                self.valid_moves.append(index - 9)

        if self.board[index] == "p":
            if index // 8 == 1:
                if self.board[index + 16] == ".":
                    self.valid_moves.append(index + 16)
            if self.board[index + 8] == ".":
                self.valid_moves.append(index + 8)
            if self.board[index + 7] != ".":
                self.valid_moves.append(index + 7)
            if self.board[index + 9] != ".":
                self.valid_moves.append(index + 9)
