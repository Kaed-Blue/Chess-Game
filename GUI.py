import pygame
from Engine import Engine

pygame.init()
clock = pygame.time.Clock()
engine = Engine()

windows_width = 700
cell_size = windows_width // 8

rows = windows_width // cell_size
cols = windows_width // cell_size

screen = pygame.display.set_mode((windows_width, windows_width))


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


images = load_assets((cell_size, cell_size))


def draw_board():
    screen.fill((133, 94, 66))
    index = 0
    for row in range(8):
        for col in range(8):
            Rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 0), Rect, 1)

            piece_info, index = engine.get_piece(index)
            if piece_info != ".":
                screen.blit(images[piece_info], (col * cell_size, row * cell_size))
            index += 1
    highlight_valid_moves()
    highlight_in_check()


def highlight_in_check():
    if engine.king_in_check_index:
        index = engine.king_in_check_index
        row, col = engine.get_position_from_index(index)
        Rect = pygame.Rect(
            (col * cell_size) + 10,
            (row * cell_size) + 10,
            cell_size - 20,
            cell_size - 20,
        )
        pygame.draw.rect(screen, (200, 50, 0), Rect, 2)


def highlight_valid_moves():  # TODO: make engine return row and col directly
    if engine.first_selection:
        for index in engine.valid_moves:
            row, col = engine.get_position_from_index(index)
            Rect = pygame.Rect(
                (col * cell_size) + 10,
                (row * cell_size) + 10,
                cell_size - 20,
                cell_size - 20,
            )
            if engine.board[index] == ".":
                pygame.draw.rect(screen, (0, 255, 0), Rect, 2)
            else:
                pygame.draw.rect(screen, (255, 0, 0), Rect, 2)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            engine.start(event.pos, cell_size)

    draw_board()
    pygame.display.flip()
    clock.tick(10)

pygame.quit()

# TODO: add hower highlighting
# TODO: make board look better
