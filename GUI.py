import pygame
from Engine import board
from Engine import get_valid_moves

pygame.init()


windows_width = 800
windows_height = 800
cell_size = windows_width / 8

rows = windows_width // cell_size
cols = windows_height // cell_size

screen = pygame.display.set_mode((windows_width, windows_height))


def load_assets(size):
    image_paths = {
        "b": "assets/black_bishop.png",
        "B": "assets/white_bishop.png",
        "k": "assets/black_king.png",
        "K": "assets/white_king.png",
        "p": "assets/black_pawn.png",
        "P": "assets/white_pawn.png",
        "q": "assets/black_queen.png",
        "Q": "assets/white_queen.png",
        "n": "assets/black_knight.png",
        "N": "assets/white_knight.png",
        "r": "assets/black_rook.png",
        "R": "assets/white_rook.png",
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


def draw_board(board):
    screen.fill((133, 94, 66))
    cnt = 0
    for row in range(8):
        for col in range(8):
            Rect = pygame.Rect(row * cell_size, col * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 0), Rect, 2)

            if board[cnt] != ".":
                screen.blit(images[board[cnt]], (col * cell_size, row * cell_size))
            cnt += 1


draw_board(board)


delta_pos = {"first_click": "", "second_click": ""}


def move_pieces(click_pos):
    global delta_pos
    selected_col = click_pos[0] // 100
    selected_row = click_pos[1] // 100
    index = (selected_row * 8) + selected_col
    # NOT DYNAMIC don't change the board size #TODO: get the click position dynamiclly
    if delta_pos["first_click"] == "":
        if board[index] != ".":
            delta_pos["first_click"] = index
            get_valid_moves(index)
    else:
        delta_pos["second_click"] = index

        if board[delta_pos["second_click"]].isalpha():
            if (
                board[delta_pos["first_click"]].isupper()
                == board[delta_pos["second_click"]].isupper()
            ):

                delta_pos["first_click"] = delta_pos["second_click"]
                delta_pos["second_click"] = ()
                return

        board[delta_pos["second_click"]] = board[delta_pos["first_click"]]
        board[delta_pos["first_click"]] = "."
        draw_board(board)

        # print(delta_pos)
        delta_pos["first_click"] = ""
        delta_pos["second_click"] = ""


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            move_pieces(event.pos)

    pygame.display.flip()

pygame.quit()
