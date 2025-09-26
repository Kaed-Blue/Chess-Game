class Engine:
    def __init__(self):
        # fmt: off
        self.board = [
        "x","x","x","x","x","x","x","x","x","x",
        "x","r","n","b","q","k","b","n","r","x",    
        "x","p","p","p","p","p","p","p","p","x",
        "x",".",".",".",".",".",".",".",".","x",
        "x",".",".",".",".",".",".",".",".","x",
        "x",".",".",".",".",".",".",".",".","x",
        "x",".",".",".",".",".",".",".",".","x",
        "x","P","P","P","P","P","P","P","P","x",
        "x","R","N","B","Q","K","B","N","R","x",
        "x","x","x","x","x","x","x","x","x","x",]
        # fmt: on
        self.delta_pos = {"first_click": "", "second_click": ""}
        self.valid_moves = []
        self.first_selection = None  # TODO: try to make selection vars local
        self.second_selection = None

    def get_piece(self, index):
        return self.board[index]

    def get_index_from_position(self, click_pos):
        index = (
            (((click_pos[1] // 100) * 8) + (click_pos[0] // 100))
            + ((click_pos[1] // 100) * 2)
            + 11
        )
        # NOT DYNAMIC don't change the board size #TODO: get the click position dynamiclly
        # selected_row = click_pos[1] // 100
        # selected_col = click_pos[0] // 100
        # self.get_selections(index)
        return index

    def get_selections(self, index):
        if self.first_selection == None:
            if self.board[index] != ".":
                self.first_selection = index
                self.get_valid_moves(self.first_selection)
                print(self.valid_moves)
                # highlight_valid_moves(self.valid_moves)
        else:
            self.second_selection = index

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

    def move_pieces(self):
        if self.second_selection in self.valid_moves:
            self.board[self.second_selection] = self.board[self.first_selection]
            self.board[self.first_selection] = "."

    def clear_values(self):
        self.first_selection = None
        self.second_selection = None
        self.valid_moves = []

    def get_valid_moves(self, index):
        self.valid_moves = []
        piece_movements = {
            "rook": [8, -8, 1, -1],
            "bishop": [9, -9, 7, -7],
            "queen": [8, -8, 1, -1, 9, -9, 7, -7],
        }

        if self.board[index] == "P":
            if index // 10 == 7:
                if self.board[index - 20] == ".":
                    self.valid_moves.append(index - 20)
            if self.board[index - 10] == ".":
                self.valid_moves.append(index - 10)
            if self.board[index - 9] != "." and self.board[index - 9] != "x":
                self.valid_moves.append(index - 9)
            if self.board[index - 11] != "." and self.board[index - 11] != "x":
                self.valid_moves.append(index - 11)

        if self.board[index] == "p":
            if index // 10 == 2:
                if self.board[index + 20] == ".":
                    self.valid_moves.append(index + 20)
            if self.board[index + 10] == ".":
                self.valid_moves.append(index + 10)
            if self.board[index + 9] != "." and self.board[index + 9] != "x":
                self.valid_moves.append(index + 9)
            if self.board[index + 11] != "." and self.board[index + 11] != "x":
                self.valid_moves.append(index + 11)

        if self.board[index] == "n" or self.board[index] == "N":
            if self.board[index - 21] != "x":
                self.valid_moves.append(index - 21)
            if self.board[index - 19] != "x":
                self.valid_moves.append(index - 19)
            if self.board[index - 12] != "x":
                self.valid_moves.append(index - 12)
            if self.board[index - 8] != "x":
                self.valid_moves.append(index - 8)
            if self.board[index + 8] != "x":
                self.valid_moves.append(index + 8)
            if self.board[index + 12] != "x":
                self.valid_moves.append(index + 12)
            if len(self.board) > index + 19:
                if self.board[index + 19] != "x":
                    self.valid_moves.append(index + 19)
            if len(self.board) > index + 21:
                if self.board[index + 21] != "x":
                    self.valid_moves.append(index + 21)

            # -21, -19, -12, -8, +8, +12, +19, +21

    def start(self, click_pos):
        index = self.get_index_from_position(click_pos)
        self.get_selections(index)
        if self.second_selection:
            self.is_same_color()
            self.move_pieces()
            self.clear_values()
