import pygame
import os

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
                                    "piece_color": "white",
                                }
                            )
                        elif row == 0 or row == 1:
                            cell_dict.update(
                                {
                                    "occupied": True,
                                    "piece_type": piece_type,
                                    "piece_color": "black",
                                }
                            )

            board[row].append(cell_dict)


init_board()


def load_assets(size):
    image_paths = {
        "black_bishop": "assets/black_bishop.png",
        "white_bishop": "assets/white_bishop.png",
        "black_king": "assets/black_king.png",
        "white_king": "assets/white_king.png",
        "black_pawn": "assets/black_pawn.png",
        "white_pawn": "assets/white_pawn.png",
        "black_queen": "assets/black_queen.png",
        "white_queen": "assets/white_queen.png",
        "black_knight": "assets/black_knight.png",
        "white_knight": "assets/white_knight.png",
        "black_rook": "assets/black_rook.png",
        "white_rook": "assets/white_rook.png",
    }
    processed_images = {}
    for name, path in image_paths.items():
        try:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, size)
            processed_images[name] = img
        except pygame.error as error:
            print(f"failed to load {name} from {path}: {error}")
    return processed_images


images = load_assets((100, 100))

# black_bishop = images["black_bishop"]
# white_bishop = images["white_bishop"]
# black_king = images["black_king"]
# white_king = images["white_king"]
# black_pawn = images["black_pawn"]
# white_pawn = images["white_pawn"]
# black_knight = images["black_knight"]
# white_knight = images["white_knight"]
# black_queen = images["black_queen"]
# white_queen = images["white_queen"]
# black_rook = images["black_rook"]
# white_rook = images["white_rook"]


def draw_board():
    screen.fill((59, 49, 16))

    for row in range(int(rows)):
        for col in range(int(cols)):
            piece_info = []
            Rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 0), Rect, 2)
            if board[row][col]["occupied"] == True:
                piece_type = board[row][col]["piece_type"]
                piece_color = board[row][col]["piece_color"]
                piece_info = [piece_color, piece_type]
                piece_info = "_".join(piece_info)
                screen.blit(images[piece_info], (col * cell_size, row * cell_size))
    pygame.display.update()


draw_board()


def get_acceptable_moves():
    pass


def move_pieces():
    pass


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
