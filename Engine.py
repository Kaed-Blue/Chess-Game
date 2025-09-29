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
        self.valid_moves = []
        self.first_selection = None
        self.second_selection = None
        self.is_white_turn = True

    def get_piece(self, index):
        while self.board[index] == "x":
            index += 1
        return self.board[index], index

    def get_index_from_position(self, click_pos, cell_size):
        index = (
            (((click_pos[1] // cell_size) * 8) + (click_pos[0] // cell_size))
            + ((click_pos[1] // cell_size) * 2)  # index offset correction
            + 11
        )
        return index

    def manage_turn(self, index, order):
        if order == "check_turn":
            if self.board[index].isupper() and self.is_white_turn:
                return True
            if self.board[index].isupper() and not self.is_white_turn:
                return False
            if not self.board[index].isupper() and self.is_white_turn:
                return False
            if not self.board[index].isupper() and not self.is_white_turn:
                return True

        if order == "pass_turn":
            self.is_white_turn = not self.is_white_turn

    def get_selections(self, index):
        if self.manage_turn(index, "check_turn") or self.board[index] == ".":
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
            self.manage_turn(None, "pass_turn")

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
        row = int(len(self.board) ** (1 / 2))
        piece_movements = {  # TODO: make movement even more abstracted (and clean)
            "rook": [row, -row, 1, -1],
            "bishop": [row + 1, -row - 1, row - 1, -row + 1],
            "queen_king": [row, -row, 1, -1, row + 1, -row - 1, row - 1, -row + 1],
            "knight": [(2 * row) + 1, (2 * row) - 1, row + 2, row - 2, -row + 2, -row - 2, (2 * -row) + 1, (2 * -row) - 1,], # fmt: skip
        }

        if self.board[index].lower() == "p":
            if self.board[index] == "P":
                move = -(row)
                diag_move = [-(row + 1), -(row - 1)]
            else:
                move = row
                diag_move = [row + 1, row - 1]

            rank = index // 10
            if rank == 7 or rank == 2:
                if self.board[index + (2 * move)] == ".":
                    self.valid_moves.append(index + (2 * move))
            if self.board[index + move] == ".":
                self.valid_moves.append(index + move)

            for move in diag_move:
                if self.board[index + move] != "." and not self.is_same_color(
                    index, index + move
                ):
                    self.valid_moves.append(index + move)

        if self.board[index] == "n" or self.board[index] == "N":
            for move in piece_movements["knight"]:
                if index + move < len(self.board):
                    if self.board[index + move] != "x" and not self.is_same_color(
                        index, index + move
                    ):
                        self.valid_moves.append(index + move)

        if self.board[index].lower() == "r":
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

        if self.board[index].lower() == "b":
            for move in piece_movements["bishop"]:
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

        if self.board[index].lower() == "q":
            for move in piece_movements["queen_king"]:
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

        if self.board[index].lower() == "k":
            for move in piece_movements["queen_king"]:
                if index + move < len(self.board):
                    if self.board[index + move] != "x" and not self.is_same_color(
                        index, index + move
                    ):
                        self.valid_moves.append(index + move)

    def is_check(self, king_index):
        pass

    def start(self, click_pos, cell_size):
        index = self.get_index_from_position(click_pos, cell_size)
        self.get_selections(index)
        if self.second_selection:
            self.is_same_color(self.first_selection, self.second_selection)
            self.move_pieces()
