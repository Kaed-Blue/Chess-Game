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
        self.legal_moves = []
        self.history = []
        self.first_selection = None
        self.second_selection = None
        self.is_white_turn = True
        self.king_pos = {"white_king": 85, "black_king": 15}
        self.one_row = int(len(self.board) ** (1 / 2))
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
                    self.get_legal_moves(self.first_selection)

        else:
            self.second_selection = index
            if self.is_same_color(self.first_selection, self.second_selection):
                self.manage_values("replace")
                self.get_legal_moves(self.first_selection)

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
        if self.second_selection in self.legal_moves:
            self.track_king_pos(self.first_selection, self.second_selection)
            self.add_history(self.first_selection, self.second_selection)
            self.board[self.second_selection] = self.board[self.first_selection]
            self.board[self.first_selection] = "."
            self.manage_game_state()

    def manage_game_state(self):
        self.make_promotion(self.second_selection)
        self.manage_turn(None, "pass_turn")
        self.in_check()
        self.manage_values("clear")

    def add_history(self, from_index, to_index):
        piece_type = self.board[from_index]
        taken = self.board[to_index] if self.board[to_index] != '.' else None
        last_move = (piece_type, from_index, to_index, taken)
        self.history.append(last_move)
        print(last_move)

    def make_promotion(self, index, promote_to=None):
        rank = index // 10
        white_piece = self.is_white(index)
        if self.board[index].lower() == "p" and rank in (1, 8):
            if promote_to is None:
                self.board[index] = "Q" if white_piece else "q"
            else:
                self.board[index] = promote_to.upper() if white_piece else promote_to.lower()
            

    def track_king_pos(self, first_selection, second_selection):
        if self.board[first_selection].lower() == "k":
            if self.is_white_turn:
                self.king_pos["white_king"] = second_selection
            else:
                self.king_pos["black_king"] = second_selection

    def in_check(self):
        king_key = "white_king" if self.is_white_turn else "black_king"
        king_pos = self.king_pos[king_key]
        if self.under_attack(king_pos):
            self.king_in_check_index = king_pos
            return True
        self.king_in_check_index = None
        return False

    def under_attack(self, index):
        if self.is_white_turn:
            row = -(self.one_row)
        else:
            row = self.one_row

        piece_movements = {  # TODO: add king
            "rook": [row, -row, 1, -1],
            "bishop": [row + 1, -row - 1, row - 1, -row + 1],
            "knight": [(2 * row) + 1, (2 * row) - 1, row + 2, row - 2, -row + 2, -row - 2, (2 * -row) + 1, (2 * -row) - 1,], # fmt: skip
            "king": [row, -row, 1, -1, row + 1, -row -1, row - 1, -row + 1]
        }

        for move in piece_movements["rook"]:
            i = 1
            while self.board[index + move] != "x" and self.board[index + move] == ".":
                move += move // i
                i += 1
            if (
                self.board[index + move].lower() == "r"
                or self.board[index + move].lower() == "q"
            ) and self.board[index + move].isupper() != self.is_white_turn:
                return True

        for move in piece_movements["bishop"]:
            i = 1
            while self.board[index + move] != "x" and self.board[index + move] == ".":
                move += move // i
                i += 1
            if (
                self.board[index + move].lower() == "b"
                or self.board[index + move].lower() == "q"
            ) and self.board[index + move].isupper() != self.is_white_turn:
                return True

        for move in piece_movements["knight"]:
            if index + move < len(self.board):
                if (
                    self.board[index + move].lower() == "n"
                    and self.board[index + move].isupper() != self.is_white_turn
                ):
                    return True
                
        # for move in piece_movements["king"]:
        #     if self.board

        for move in [index + row + 1, index + row - 1]:
            if (
                self.board[move].lower() == "p"
                and self.board[move].isupper() != self.is_white_turn
            ):
                return True

    def manage_values(self, order):
        if order == "replace":
            self.first_selection = self.second_selection
            self.second_selection = None
            self.legal_moves = []

        elif order == "clear":
            self.first_selection = None
            self.second_selection = None
            self.legal_moves = []


    def get_psudo_legal_moves(self, index):
        psudo_legal_moves = []
        row = self.one_row
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
            if self.board[index + move] == ".":
                psudo_legal_moves.append(index + move)
                if rank == 7 or rank == 2:
                    if self.board[index + (2 * move)] == ".":
                        psudo_legal_moves.append(index + (2 * move))

            for move in diag_move:
                if self.board[index + move] != "." and not self.is_same_color(
                    index, index + move
                ):
                    psudo_legal_moves.append(index + move)

        elif self.board[index] == "n" or self.board[index] == "N":
            for move in piece_movements["knight"]:
                if index + move < len(self.board):
                    if self.board[index + move] != "x" and not self.is_same_color(
                        index, index + move
                    ):
                        psudo_legal_moves.append(index + move)

        elif self.board[index].lower() == "r":
            for move in piece_movements["rook"]:
                i = 1
                while self.board[index + move] != "x" and not self.is_same_color(
                    index, index + move
                ):
                    psudo_legal_moves.append(index + move)
                    if self.board[index + move] != "." and not self.is_same_color(
                        index, index + move
                    ):
                        break
                    move += move // i
                    i += 1

        elif self.board[index].lower() == "b":
            for move in piece_movements["bishop"]:
                i = 1
                while self.board[index + move] != "x" and not self.is_same_color(
                    index, index + move
                ):
                    psudo_legal_moves.append(index + move)
                    if self.board[index + move] != "." and not self.is_same_color(
                        index, index + move
                    ):
                        break
                    move += move // i
                    i += 1

        elif self.board[index].lower() == "q":
            for move in piece_movements["queen_king"]:
                i = 1
                while self.board[index + move] != "x" and not self.is_same_color(
                    index, index + move
                ):
                    psudo_legal_moves.append(index + move)
                    if self.board[index + move] != "." and not self.is_same_color(
                        index, index + move
                    ):
                        break
                    move += move // i
                    i += 1

        elif self.board[index].lower() == "k":
            for move in piece_movements["queen_king"]:
                if index + move < len(self.board):
                    if self.board[index + move] != "x" and not self.is_same_color(
                        index, index + move
                    ):
                        psudo_legal_moves.append(index + move)
        return psudo_legal_moves

    def get_legal_moves(self, index):
        psudo_legal_moves = self.get_psudo_legal_moves(index)
        for move in psudo_legal_moves:
            if not self.check_in_psudoboard(index, move):
                self.legal_moves.append(move)

    def check_in_psudoboard(self, origin, destination):
        temp = self.board[destination]
        self.track_king_pos(origin, destination)
        self.board[destination] = self.board[origin]
        self.board[origin] = "."
        flag = self.in_check()
        self.track_king_pos(destination, origin)
        self.board[origin] = self.board[destination]
        self.board[destination] = temp
        return flag
    
    def start(self, click_pos, cell_size):
        index = self.get_index_from_position(click_pos, cell_size)
        self.get_selections(index)
        if self.second_selection:
            self.is_same_color(self.first_selection, self.second_selection)
            self.move_pieces()

 # TODO: move history and undo
