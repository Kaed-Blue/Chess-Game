import pygame

pygame.init()

windows_width = 800
windows_height = 800
cell_size = windows_height / 8

rows = windows_width // cell_size
cols = windows_height // cell_size

screen = pygame.display.set_mode((windows_width, windows_height))


def init_board():
    # fmt: off
    pieces_dict = {
        "rook": [(0, 0), (7, 7), (7, 0), (0, 7)],
        "knight": [(0, 1), (0, 6), (7, 1), (7, 6)],
        "queen": [(0, 3), (7, 3)],
        "king": [(0, 4), (7, 4)],
        "bishop": [(0, 2), (0, 5), (7, 2), (7, 5)],
        "pawn": [(1, 0), (1, 1), (1, 2),(1, 3),
                 (1, 4), (1, 5), (1, 6), (1, 7),
                 (6, 0),(6, 1), (6, 2), (6, 3),
                 (6, 4), (6, 5), (6, 6), (6, 7),
        ],
    }
    # fmt: on

    board = []
    for row in range(int(rows)):  # col = x, row = y
        board.append([])
        for col in range(int(cols)):
            cell_dict = {
                "occupied": False,
                "piece_type": "",
                "piece_color": "",
            }
            for piece_type, piece_pos in pieces_dict.items():
                for pos in piece_pos:
                    if pos == (row, col):
                        if row == 6 or row == 7:
                            cell_dict.update(
                                {
                                    "occupied": True,
                                    "piece_type": piece_type,
                                    "piece_color": "black",
                                }
                            )
                        elif row == 0 or row == 1:
                            cell_dict.update(
                                {
                                    "occupied": True,
                                    "piece_type": piece_type,
                                    "piece_color": "white",
                                }
                            )

            board[row].append(cell_dict)
    print(board)


init_board()


def draw_board():
    pass


def get_acceptable_moves():
    pass


def move_pieces():
    pass


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
