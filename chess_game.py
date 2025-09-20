import pygame

pygame.init()

windows_width = 800
windows_height = 800
cell_size = windows_height / 8

rows = windows_width // cell_size
cols = windows_height // cell_size

screen = pygame.display.set_mode((windows_width, windows_height))

# fmt: off
pieces_dict = {
    "rook": [(0, 0), (7, 7), (7, 0), (0, 7)],
    "knight": [(0, 1), (0, 6), (7, 1), (7, 6)],
    "queen": [(0, 3), (7, 3)],
    "king": [(0, 4), (7, 4)],
    "bishop": [(0, 2), (0, 5), (7, 2), (7, 5)],
    "pawn": [(1, 0), (1, 1), (1, 2), (1, 3),
             (1, 4), (1, 5), (1, 6), (1, 7),
             (6, 0), (6, 1), (6, 2), (6, 3),
             (6, 4), (6, 5), (6, 6), (6, 7),
             ],
    }
# fmt: on

board = []


def init_board():

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

# load assets
black_bishop = pygame.image.load("assets/black_bishop.png")
white_bishop = pygame.image.load("assets/white_bishop.png")
black_king = pygame.image.load("assets/black_king.png")
white_king = pygame.image.load("assets/white_king.png")
black_pawn = pygame.image.load("assets/black_pawn.png")
white_pawn = pygame.image.load("assets/white_pawn.png")
black_queen = pygame.image.load("assets/black_queen.png")
white_queen = pygame.image.load("assets/white_queen.png")
black_knight = pygame.image.load("assets/black_knight.png")
white_knight = pygame.image.load("assets/white_knight.png")
black_rook = pygame.image.load("assets/black_rook.png")
white_rook = pygame.image.load("assets/white_rook.png")

black_bishop = black_bishop.convert_alpha()
white_bishop = white_bishop.convert_alpha()
black_king = black_king.convert_alpha()
white_king = white_king.convert_alpha()
black_pawn = black_pawn.convert_alpha()
white_pawn = white_pawn.convert_alpha()
black_queen = black_queen.convert_alpha()
white_queen = white_queen.convert_alpha()
black_knight = black_knight.convert_alpha()
white_knight = white_knight.convert_alpha()
black_rook = black_rook.convert_alpha()
white_rook = white_rook.convert_alpha()


def draw_board():
    screen.fill((0, 0, 0))

    for row in range(int(rows)):
        for col in range(int(cols)):
            if board[row][col]["occupied"] == True:
                pass


def get_acceptable_moves():
    pass


def move_pieces():
    pass


running = True
while running:
    screen.fill((100, 100, 100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(black_bishop, (0, 0))
    screen.blit(white_bishop, (0, 100))
    screen.blit(black_rook, (0, 200))
    screen.blit(white_king, (0, 300))
    screen.blit(black_king, (0, 400))

    pygame.display.flip()

pygame.quit()
