import pygame
import os

pygame.init()

windows_width = 800  # default = 800
windows_height = 800  # default = 800
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
                "piece_type": "",
                "piece_color": "",
            }
            for piece_type, piece_pos in pieces_dict.items():
                for pos in piece_pos:
                    if pos == (row, col):
                        if row == 6 or row == 7:
                            cell_dict.update(
                                {
                                    "piece_type": piece_type,
                                    "piece_color": "white",
                                }
                            )
                        elif row == 0 or row == 1:
                            cell_dict.update(
                                {
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


def draw_board():
    screen.fill((133, 94, 66))

    for row in range(int(rows)):
        for col in range(int(cols)):
            piece_info = []
            Rect = pygame.Rect(row * cell_size, col * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 0), Rect, 2)
            if board[row][col]["piece_type"]:
                piece_type = board[row][col]["piece_type"]
                piece_color = board[row][col]["piece_color"]
                piece_info = [piece_color, piece_type]
                piece_info = "_".join(piece_info)
                screen.blit(images[piece_info], (col * cell_size, row * cell_size))
    pygame.display.update()


draw_board()
valid_moves = []


def get_valid_moves(piece_pos):

    piece_type = board[piece_pos[0]][piece_pos[1]]["piece_type"]
    piece_color = board[piece_pos[0]][piece_pos[1]]["piece_color"]

    global valid_moves

    if piece_type == "pawn":

        print(f"{piece_color}_{piece_type} at {piece_pos}")  # debug
        if piece_color == "white":
            if piece_pos[0] == 6:
                if not board[piece_pos[0] - 1][piece_pos[1]]["piece_type"]:
                    valid_moves.append((piece_pos[0] - 1, piece_pos[1]))
                if not board[piece_pos[0] - 2][piece_pos[1]]["piece_type"]:
                    valid_moves.append((piece_pos[0] - 2, piece_pos[1]))
                if board[piece_pos[0] - 1][piece_pos[1] + 1]["piece_type"]:
                    valid_moves.append((piece_pos[0] - 1, piece_pos[1] + 1))
                if board[piece_pos[0] - 1][piece_pos[1] - 1]["piece_type"]:
                    valid_moves.append((piece_pos[0] - 1, piece_pos[1] - 1))
            else:
                if not board[piece_pos[0] - 1][piece_pos[1]]["piece_type"]:
                    valid_moves.append((piece_pos[0] - 1, piece_pos[1]))
                if board[piece_pos[0] - 1][piece_pos[1] + 1]["piece_type"]:
                    valid_moves.append((piece_pos[0] - 1, piece_pos[1] + 1))
                if board[piece_pos[0] - 1][piece_pos[1] - 1]["piece_type"]:
                    valid_moves.append((piece_pos[0] - 1, piece_pos[1] - 1))
            return

        if piece_color == "black":
            pass
    else:
        print("no")


delta_pos = {"first_click": (), "second_click": ()}


def move_pieces(click_pos):
    global delta_pos
    global valid_moves
    selected_col = click_pos[0] // 100
    selected_row = click_pos[1] // 100
    # NOT DYNAMIC don't change the board size #TODO: get the click position dynamiclly

    if not delta_pos["first_click"]:
        if board[selected_row][selected_col]["piece_type"]:
            delta_pos["first_click"] = (selected_row, selected_col)
            get_valid_moves(delta_pos["first_click"])
            print(valid_moves)

    else:
        delta_pos["second_click"] = (selected_row, selected_col)
        first_click_row = delta_pos["first_click"][0]
        first_click_col = delta_pos["first_click"][1]
        second_click_row = delta_pos["second_click"][0]
        second_click_col = delta_pos["second_click"][1]

        if (
            board[first_click_row][first_click_col]["piece_color"]
            == board[second_click_row][second_click_col]["piece_color"]
        ):
            delta_pos["first_click"] = delta_pos["second_click"]
            delta_pos["second_click"] = ()
            return

        # acceptable_moves = get_acceptable_moves(delta_pos["first_click"])
        # print(acceptable_moves)
        if delta_pos["second_click"] in valid_moves:
            temp = board[first_click_row][first_click_col]["piece_type"]
            board[second_click_row][second_click_col]["piece_type"] = temp
            board[first_click_row][first_click_col]["piece_type"] = ""

            temp = board[first_click_row][first_click_col]["piece_color"]
            board[second_click_row][second_click_col]["piece_color"] = temp
            board[first_click_row][first_click_col]["piece_color"] = ""

            delta_pos["first_click"] = ()
            delta_pos["second_click"] = ()
            valid_moves = []
            draw_board()


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            move_pieces(event.pos)

    pygame.display.flip()

pygame.quit()
