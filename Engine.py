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

    def get_piece(self, index):
        return self.board[index]

    def move_pieces(self, click_pos):
        selected_col = click_pos[0] // 100
        selected_row = click_pos[1] // 100
        index = (selected_row * 8) + selected_col
        # NOT DYNAMIC don't change the board size #TODO: get the click position dynamiclly

        if self.delta_pos["first_click"] == "":
            if self.board[index] != ".":
                self.delta_pos["first_click"] = index
                self.get_valid_moves(index)
        else:
            self.delta_pos["second_click"] = index
            print(self.delta_pos)

            if self.board[self.delta_pos["second_click"]].isalpha():
                if (
                    self.board[self.delta_pos["first_click"]].isupper()
                    == self.board[self.delta_pos["second_click"]].isupper()
                ):

                    print("happend")
                    self.delta_pos["first_click"] = self.delta_pos["second_click"]
                    self.delta_pos["second_click"] = ""
                    self.get_valid_moves(int(self.delta_pos["first_click"]))
                    return

            if self.delta_pos["second_click"] in self.valid_moves:
                self.board[self.delta_pos["second_click"]] = self.board[self.delta_pos["first_click"]] # fmt: skip
                self.board[self.delta_pos["first_click"]] = "."

            # print(self.delta_pos)
            self.delta_pos["first_click"] = ""
            self.delta_pos["second_click"] = ""
            self.valid_moves = []

    def get_valid_moves(self, index):
        piece_movements = {}
        if self.board[index] == "P":
            if self.board[index - 8] == ".":
                self.valid_moves.append(index - 8)


# draw_board(board=board)
