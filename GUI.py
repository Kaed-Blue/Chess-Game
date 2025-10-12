import pygame
from Engine import Engine

pygame.init()
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()
engine = Engine()

windows_width = 760
windows_height = 810
cell_size = windows_width // 8

rows = windows_width // cell_size  # you can just put 8
cols = windows_width // cell_size

screen = pygame.display.set_mode((windows_width, windows_height))


def load_assets(size):
    image_paths = {
        "b": "assets/bb.png",
        "B": "assets/wb.png",
        "k": "assets/bk.png",
        "K": "assets/wk.png",
        "p": "assets/bp.png",
        "P": "assets/wp.png",
        "q": "assets/bq.png",
        "Q": "assets/wq.png",
        "n": "assets/bn.png",
        "N": "assets/wn.png",
        "r": "assets/br.png",
        "R": "assets/wr.png",
        "undo_button": "assets/undo.png",
        "redo_button": "assets/redo.png",
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


class Button:
    def __init__(self, x, y, image, scale):
        width, height = image.get_width(), image.get_height()
        self.image = pygame.transform.scale(
            image, (int((width * scale)), int((height * scale)))
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw_button(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def action(self):
        if pygame.mouse.get_pressed()[0] == 1:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos) and self.clicked == False:
                self.clicked = True
                return True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return False


undo_button = Button(20, 750, images["undo_button"], 0.65)
redo_button = Button(100, 750, images["redo_button"], 0.65)

def draw_board():
    screen.fill((133, 94, 66))
    index = 0
    alter = False
    for row in range(8):
        alter = not alter
        for col in range(8):
            Rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            if alter:
                pygame.draw.rect(
                    screen, (100, 70, 40), Rect, 0
                )  # (100, 70, 40), (140, 90, 60)
            else:
                pygame.draw.rect(
                    screen, (181, 136, 99), Rect, 0
                )  # (181, 136, 99), (70, 40, 20)
            alter = not alter

            pygame.draw.rect(screen, (0, 0, 0), Rect, 1)

            piece_info, index = engine.get_piece(index)
            if piece_info != ".":
                screen.blit(images[piece_info], (col * cell_size, row * cell_size))
            index += 1
    highlight_legal_moves()
    highlight_in_check()
    undo_button.draw_button()
    redo_button.draw_button()


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


def highlight_legal_moves():
    if engine.first_selection:
        for index in engine.legal_moves:
            row, col = engine.get_position_from_index(index)
            Rect = pygame.Rect(
                (col * cell_size) + 10,
                (row * cell_size) + 10,
                cell_size - 20,
                cell_size - 20,
            )
            if engine.board[index] == ".":
                pygame.draw.rect(screen, (0, 255, 0), Rect, 2)
            elif engine.board[index] != "." and engine.board[index] != "x":
                pygame.draw.rect(screen, (255, 0, 0), Rect, 2)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            engine.start(event.pos, cell_size)

    if undo_button.action():
        engine.undo()
    if redo_button.action():
        engine.redo()

    draw_board()
    pygame.display.flip()
    clock.tick(20)

pygame.quit()

# TODO: add hower highlighting
# TODO: add drag and drop
# TODO: add selective promotion
