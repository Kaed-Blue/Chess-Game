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
        return index

    def get_selections(self, index):
        if self.first_selection == None:
            if self.board[index] != ".":
                self.first_selection = index
                self.get_valid_moves(self.first_selection)
                print(self.valid_moves)

        else:
            self.second_selection = index
            if self.is_same_color(self.first_selection, self.second_selection):
                self.manage_values("replace")
                self.get_valid_moves(self.first_selection)
                print(self.valid_moves)

    def is_same_color(self, index_1, index_2):
        if self.board[index_2].isalpha():
            if self.board[index_1].isupper() == self.board[index_2].isupper():
                return True
            else:
                return False
        else:
            return False

    def move_pieces(self):
        if self.second_selection in self.valid_moves:
            self.board[self.second_selection] = self.board[self.first_selection]
            self.board[self.first_selection] = "."
            self.manage_values("clear")

    def manage_values(self, order):
        if order == "replace":
            self.first_selection = self.second_selection
            self.second_selection = None

        elif order == "clear":
            self.first_selection = None
            self.second_selection = None
            self.valid_moves = []

    def get_valid_moves(self, index):
        self.valid_moves = []
        piece_movements = {
            "rook": [10, -10, 1, -1],
            "bishop": [11, -11, 9, -9],
            "queen": [10, -10, 1, -1, 11, -11, 9, -9],
            "knight": [21, 19, 12, 8, -8, -12, -19, -21],
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
            for move in piece_movements["knight"]:
                if index + move < len(self.board):
                    if self.board[index + move] != "x" and not self.is_same_color(
                        index, index + move
                    ):
                        self.valid_moves.append(index + move)

        if self.board[index] == "r" or self.board[index] == "R":
            for move in piece_movements["rook"]:
                i = 1
                while self.board[index + move] != "x" and not self.is_same_color(
                    index, index + move
                ):
                    self.valid_moves.append(index + move)
                    if self.board[index + move] != "." and not self.is_same_color(
                        index, index + move
                    ):
                        break
                    move += move // i
                    i += 1

    def start(self, click_pos):
        index = self.get_index_from_position(click_pos)
        self.get_selections(index)
        if self.second_selection:
            self.is_same_color(self.first_selection, self.second_selection)
            self.move_pieces()
