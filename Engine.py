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
        self.king_pos = {"white_king": 85, "black_king": 15}
        self.row = int(len(self.board) ** (1 / 2))
        self.king_in_check_index = None

    def get_piece(self, index):  # TODO: refactor
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

    def get_position_from_index(self, index):
        row = (index // 10) - 1
        col = (index % 10) - 1
        return row, col

    def manage_turn(self, index, order):
        if order == "check_turn":
            piece_is_white = self.board[index].isupper()
            return piece_is_white == self.is_white_turn

        if order == "pass_turn":
            self.is_white_turn = not self.is_white_turn

    def get_selections(self, index):
        if self.first_selection == None:
            if self.manage_turn(index, "check_turn"):
                if self.board[index] != ".":
                    self.first_selection = index
                    self.get_valid_moves(self.first_selection)
                    # print(self.valid_moves)

        else:
            self.second_selection = index
            # print (self.second_selection)
            if self.is_same_color(self.first_selection, self.second_selection):
                self.manage_values("replace")
                self.get_valid_moves(self.first_selection)
                # print(self.valid_moves)

    def is_same_color(self, index_1, index_2):
        if self.board[index_1].isalpha() and self.board[index_2].isalpha():
            return self.board[index_1].isupper() == self.board[index_2].isupper()
        return False

    def is_white(self, index):
        if self.board[index].isupper():
            return True
        else:
            return False

    def move_pieces(self):
        if self.second_selection in self.valid_moves:
            self.track_king_pos()
            self.board[self.second_selection] = self.board[self.first_selection]
            self.board[self.first_selection] = "."
            self.manage_turn(None, "pass_turn")
            self.king_in_check_index = self.in_check()
            self.manage_values("clear")

    def track_king_pos(self):
        if self.board[self.first_selection].lower() == "k":
            if self.is_white(self.first_selection):
                self.king_pos["white_king"] = self.second_selection
            else:
                self.king_pos["black_king"] = self.second_selection

    def in_check(self):
        if not self.is_white(self.second_selection):
            if self.under_attack(self.king_pos["white_king"]):
                return self.king_pos["white_king"]
            return None
        else:
            if self.under_attack(self.king_pos["black_king"]):
                return self.king_pos["black_king"]
            return None

    def under_attack(self, index):
        if self.is_white_turn:
            row = -(self.row)
        else:
            row = self.row

        piece_movements = {
            "rook": [row, -row, 1, -1],
            "bishop": [row + 1, -row - 1, row - 1, -row + 1],
            "knight": [(2 * row) + 1, (2 * row) - 1, row + 2, row - 2, -row + 2, -row - 2, (2 * -row) + 1, (2 * -row) - 1,], # fmt: skip
        }

        for move in piece_movements["rook"]:
            i = 1
            while self.board[index + move] != "x" and self.board[index + move] == ".":
                move += move // i
                i += 1
            if (
                (self.board[index + move].lower() == "r" or self.board[index + move].lower() == "q")
                and self.board[index + move].isupper() != self.is_white_turn
            ):
                print("attacked by rook")
                return True
            
        for move in piece_movements["bishop"]:
            i = 1
            while self.board[index + move] != "x" and self.board[index + move] == ".":
                move += move // i
                i += 1
            if (
                (self.board[index + move].lower() == "b" or self.board[index + move].lower() == "q")
                and self.board[index + move].isupper() != self.is_white_turn
            ):
                print("attacked by bishop")
                return True
        
        for move in piece_movements["knight"]:
            if index + move < len(self.board):
                if (
                    self.board[index + move].lower() == "n"
                    and self.board[index + move].isupper() != self.is_white_turn
                ):
                    print("attacked by knight")
                    return True
            
        for move in [index + row + 1, index + row - 1]:
            if (
                self.board[move].lower() == "p"
                and self.board[move].isupper() != self.is_white_turn
            ):
                print("attacked by pawn")
                return True

    def manage_values(self, order):
        if order == "replace":
            self.first_selection = self.second_selection
            self.second_selection = None

        elif order == "clear":
            self.first_selection = None
            self.second_selection = None
            self.valid_moves = []

    def check_in_psudoboard(self, first_index, second_index):
        self.board[second_index] = self.board[first_index]
        self.second_selection = first_index
        self.board[first_index] = "."
        flag = self.in_check()
        self.second_selection = None
        self.board[first_index] = self.board[second_index]
        self.board[second_index] = "."
        return flag

    def get_valid_moves(self, index):
        self.valid_moves = []
        row = self.row
        piece_movements = {
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
                    if (
                        self.board[index + move] != "x"
                        and not self.is_same_color(index, index + move)
                        and not self.under_attack(index + move)
                    ):
                        self.valid_moves.append(index + move)

    def start(self, click_pos, cell_size):
        index = self.get_index_from_position(click_pos, cell_size)
        self.get_selections(index)
        if self.second_selection:
            self.is_same_color(self.first_selection, self.second_selection)
            self.move_pieces()
