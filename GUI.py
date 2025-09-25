import pygame
from Engine import Engine

pygame.init()
clock = pygame.time.Clock()
engine = Engine()

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


def draw_board():
    screen.fill((133, 94, 66))
    cnt = 0
    for row in range(8):
        for col in range(8):
            Rect = pygame.Rect(row * cell_size, col * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 0), Rect, 2)

            piece_info = engine.get_piece(cnt)
            if piece_info != ".":
                screen.blit(images[piece_info], (col * cell_size, row * cell_size))
            cnt += 1


def highlight_valid_moves():  # TODO
    if engine.first_selection:
        for index in engine.valid_moves:
            row = index // 8
            col = (index % 8) - 1
            print(row, col)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            engine.get_index_from_position(event.pos)

    # highlight_valid_moves()
    draw_board()
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
