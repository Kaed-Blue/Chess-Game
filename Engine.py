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
        self.first_selection = None
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
        else:
            self.move_pieces()

    def move_pieces(self):
        if self.second_selection in self.valid_moves:
            self.board[self.second_selection] = self.board[self.first_selection] # fmt: skip
            self.board[self.first_selection] = "."
            self.clear_values()

    def clear_values(self):
        self.first_selection = None
        self.second_selection = None
        self.valid_moves = []

    def get_valid_moves(self, index):
        piece_movements = {}
        if self.board[index] == "P":
            if self.board[index - 8] == ".":
                self.valid_moves.append(index - 8)


# draw_board(board=board)
