def compatibility_translator(order, pos=None, index=None):
    col_dict = {
        "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8,  # fmt: skip
    }
    row_dict = {
        "1": 8, "2": 7, "3": 6, "4": 5, "5": 4, "6": 3, "7": 2, "8": 1,  # fmt: skip
    }
    if order == "index_from_pos":
        col = col_dict[pos[0]]
        row = row_dict[pos[1]]
        return (row * 10) + col

    if order == "pos_from_index":
        row = index // 10
        col = index % 10
        for key, value in col_dict.items():
            if value == col:
                col = key
        for key, value in row_dict.items():
            if value == row:
                row = key
        return str(col) + str(row)
    return None


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
        self.first_selection = None
        self.second_selection = None
        self.king_in_check_index = None
        self.en_passant_able = None
        self.legal_moves = []
        self.history = []
        self.move_id = -1
        self.just_moved = False
        self.is_white_turn = True
        self.king_pos = {"white_king": 85, "black_king": 15}
        self.one_row = int(len(self.board) ** (1 / 2))

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
        if 10 < index < 89:
            return index

    def get_position_from_index(self, index):
        row = (index // 10) - 1
        col = (index % 10) - 1
        return row, col

    def manage_turn(self, order, index=None):
        if order == "check_turn":
            piece_is_white = self.board[index].isupper()
            return piece_is_white == self.is_white_turn

        if order == "pass_turn":
            self.is_white_turn = not self.is_white_turn
        return None

    def get_selections(self, index):
        self.just_moved = False
        if self.first_selection is None:
            if self.manage_turn("check_turn", index):
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
            self.pre_move_updates()
            self.board[self.second_selection] = self.board[self.first_selection]
            self.board[self.first_selection] = "."
            self.post_move_updates()
        else:
            self.legal_moves = []

    def pre_move_updates(self):
        self.track_king_pos(self.first_selection, self.second_selection)
        self.add_history(self.first_selection, self.second_selection)
        self.is_enpassant_able(self.first_selection, self.second_selection)

    def post_move_updates(self):
        self.make_promotion(self.second_selection)
        self.manage_turn("pass_turn")
        self.in_check()
        self.just_moved = True
        self.manage_values("clear")

    def add_history(self, from_index, to_index):
        self.move_id += 1
        piece_type = self.board[from_index]
        taken = self.board[to_index]
        last_move = (piece_type, from_index, to_index, taken)
        self.history.append(last_move)
        print(last_move)

    def undo(self):  # TODO: fix undo to consider promotions
        if 0 <= self.move_id < len(self.history):
            piece_type, from_index, to_index, taken = self.history[self.move_id]
            self.board[from_index] = self.board[to_index]
            self.board[to_index] = taken
            del self.history[-1]
            self.move_id -= 1
            self.manage_turn("pass_turn")

    def make_promotion(self, index, promote_to=None):
        rank = index // 10
        if self.board[index].lower() == "p" and rank in (1, 8):
            white_piece = self.is_white(index)
            if promote_to is None:
                self.board[index] = "Q" if white_piece else "q"
            else:
                self.board[index] = (
                    promote_to.upper() if white_piece else promote_to.lower()
                )

    def is_enpassant_able(self, origin, destination):
        self.en_passant_able = None
        if self.board[origin].lower() == "p":
            if (origin // 10) == 7 or (origin // 10) == 2:
                if (destination // 10) == 5 or (destination // 10) == 4:
                    self.en_passant_able = destination
                    print(self.en_passant_able)

    def track_king_pos(self, first_selection, second_selection):
        if self.board[first_selection].lower() == "k":
            if self.is_white_turn:
                self.king_pos["white_king"] = second_selection
            else:
                self.king_pos["black_king"] = second_selection

    def get_king_inturn_pos(self):
        king_key = "white_king" if self.is_white_turn else "black_king"
        return self.king_pos[king_key]

    def in_check(self):
        king_pos = self.get_king_inturn_pos()
        if self.under_attack(king_pos):
            self.king_in_check_index = king_pos
            return True
        self.king_in_check_index = None
        return False

    def under_attack(self, index):
        if self.is_white_turn:
            row = -self.one_row
        else:
            row = self.one_row

        piece_movements = {
            "rook": [row, -row, 1, -1],
            "bishop": [row + 1, -row - 1, row - 1, -row + 1],
            "knight": [(2 * row) + 1, (2 * row) - 1, row + 2, row - 2, -row + 2, -row - 2, (2 * -row) + 1,
                       (2 * -row) - 1, ],  # fmt: skip
            "king": [row, -row, 1, -1, row + 1, -row - 1, row - 1, -row + 1],
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

        for move in piece_movements["king"]:
            king_pos = self.get_king_inturn_pos()
            if index + move != king_pos:
                if self.board[index + move].lower() == "k":
                    return True

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

    def get_pseudo_legal_moves(self, index):
        pseudo_legal_moves = []
        row = self.one_row
        piece_movements = {
            "rook": [row, -row, 1, -1],
            "bishop": [row + 1, -row - 1, row - 1, -row + 1],
            "queen_king": [row, -row, 1, -1, row + 1, -row - 1, row - 1, -row + 1],
            "knight": [(2 * row) + 1, (2 * row) - 1, row + 2, row - 2, -row + 2, -row - 2, (2 * -row) + 1,
                       (2 * -row) - 1, ],  # fmt: skip
        }

        if self.board[index].lower() == "p":
            if self.board[index] == "P":
                move = -row
                diag_move = [-(row + 1), -(row - 1)]
            else:
                move = row
                diag_move = [row + 1, row - 1]

            rank = index // 10
            if self.board[index + move] == ".":
                pseudo_legal_moves.append(index + move)
                if rank == 7 or rank == 2:
                    if self.board[index + (2 * move)] == ".":
                        pseudo_legal_moves.append(index + (2 * move))

            for move in diag_move:
                if self.board[index + move] != "." and not self.is_same_color(
                    index, index + move
                ):
                    pseudo_legal_moves.append(index + move)

        elif self.board[index] == "n" or self.board[index] == "N":
            for move in piece_movements["knight"]:
                if index + move < len(self.board):
                    if self.board[index + move] != "x" and not self.is_same_color(
                        index, index + move
                    ):
                        pseudo_legal_moves.append(index + move)

        elif self.board[index].lower() == "r":
            for move in piece_movements["rook"]:
                i = 1
                while self.board[index + move] != "x" and not self.is_same_color(
                    index, index + move
                ):
                    pseudo_legal_moves.append(index + move)
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
                    pseudo_legal_moves.append(index + move)
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
                    pseudo_legal_moves.append(index + move)
                    if self.board[index + move] != "." and not self.is_same_color(
                        index, index + move
                    ):
                        break
                    move += move // i
                    i += 1

        elif self.board[index].lower() == "k":
            for move in piece_movements["queen_king"]:
                if index + move < len(self.board):

                    if (
                        self.board[index + move] != "x"
                        and not self.is_same_color(index, index + move)
                        and not self.under_attack(index + move)
                    ):
                        self.legal_moves.append(index + move)
        return pseudo_legal_moves

    def get_legal_moves(self, index):
        pseudo_legal_moves = self.get_pseudo_legal_moves(index)
        for move in pseudo_legal_moves:
            if not self.check_in_pseudoboard(index, move):
                self.legal_moves.append(move)

    def check_in_pseudoboard(self, origin, destination):
        temp = self.board[destination]
        self.track_king_pos(origin, destination)
        self.board[destination] = self.board[origin]
        self.board[origin] = "."
        flag = self.in_check()
        self.track_king_pos(destination, origin)
        self.board[origin] = self.board[destination]
        self.board[destination] = temp
        return flag

    def get_fen_string(self):
        fen = ""
        i = 0
        index = 0
        for row in range(1, 10):
            if i > 0:
                fen += str(i)
                i = 0
            fen += "/"

            for col in range(1, 11):
                if self.board[index] != "x":
                    piece = self.board[index]
                    if piece != ".":
                        if i > 0:
                            fen += str(i)
                            i = 0
                            fen += piece
                        else:
                            fen += piece
                    else:
                        i += 1
                index += 1
        return fen[2:]

    def start(self, pos, cell_size):
        index = self.get_index_from_position(pos, cell_size)
        if index:
            self.get_selections(index)
            if self.second_selection:
                self.is_same_color(self.first_selection, self.second_selection)
                self.move_pieces()
            # return self.get_fen_string()
        # else:
        # return False


#   TODO: add checkmate
#   TODO: add en passant
#   TODO: add castling
