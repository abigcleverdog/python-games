import pygame
import random
import numpy as np

pygame.init()

CELL_SIZE = 20
BOARD = 10, 20
GAME_SIZE = CELL_SIZE * BOARD[0], CELL_SIZE * BOARD[1]
WIN_SIZE = 800, 500

TOP_LEFT = (WIN_SIZE[0] - GAME_SIZE[0]) // 2, (WIN_SIZE[1] - GAME_SIZE[1]) // 2

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREY = 128, 128, 128
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
CYAN = 0, 255, 255
PURPLE = 255, 0, 255
YELLOW = 255, 255, 0

COLOR_LIST = [RED, GREEN, BLUE, CYAN, PURPLE, YELLOW]

SHAPES = {"S0": [(0, 1), (0, 2), (1, 0), (1, 1)],
          "S1": [(0, 0), (0, 1), (1, 1), (1, 2)],
          "L0": [(0, 0), (0, 1), (1, 0), (2, 0)],
          "L1": [(0, 0), (0, 1), (1, 1), (2, 1)],
          "O": [(0, 0), (0, 1), (1, 0), (1, 1)],
          "F": [(0, 0), (0, 1), (0, 2), (0, 3)]}


class Piece(object):
    def __init__(self, col, row, shape):
        self.col = col  # column
        self.row = row  # row
        self.state = 0
        self.shape = SHAPES.get(shape)
        self.rotations = self._get_rots()
        self.color = random.randint(3, 8)

    def move(self, dx=0, dy=0):
        self.col += dx
        self.row += dy

    def get_cells(self):
        res = [(self.col + x, self.row + y) for x, y in self.rotations[self.state]]
        return res

    def rotate(self, dw):
        self.state += dw
        self.state %= len(self.rotations)

    def _get_rots(self):
        res = [self.shape]
        mat = np.zeros((5, 5))
        for x, y in self.shape:
            mat[y][x] = 1
        for i in range(3):
            mat = np.rot90(mat)
            cur = [(x, y) for x in range(5) for y in range(5) if mat[y][x] == 1]
            minx = min([x for x, y in cur])
            miny = min([y for x, y in cur])
            cur = [(x - minx, y - miny) for x, y in cur]
            res.append(cur)

        return res


class Board(object):
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.board = np.zeros((row, col))

    def valid(self, piece):
        marks = piece.get_cells()
        for x, y in marks:
            if x >= self.col or x < 0:
                return False
            if y >= self.row or y < 0:
                return False
            if self.board[y][x] != 0:
                return False
        return True

    def add_piece(self, piece):
        marks = piece.get_cells()
        for x, y in marks:
            self.board[y][x] = piece.color

    def update(self):
        to_del = []
        for i, r in enumerate(self.board):
            if 0 not in r:
                to_del.append(i)
        if to_del:
            self.board = np.delete(self.board, to_del, 0)
            self.board = np.concatenate((np.zeros((len(to_del), self.col)), self.board))
        return len(to_del)

    def print(self, piece=None):
        if piece is None:
            print(self.board)
            print()
            return
        to_print = np.copy(self.board)
        marks = piece.get_cells()
        for x, y in marks:
            if 0 <= x < self.col and 0 <= y < self.row:
                to_print[y][x] = piece.color
        print(to_print)
        print()


def get_random_piece():
    shape = random.choice(list(SHAPES.keys()))
    p = Piece(4, 0, shape)
    p.rotate(random.randrange(4))
    print(shape, p.color, p.state)

    return p


def valid(board, piece):
    marks = piece.get_cells()
    for x, y in marks:
        if x >= len(board[0]) or x < 0:
            return False
        if y >= len(board) or y < 0:
            return False
        if board[y][x] != 0:
            return False
    return True


def get_color(num):
    num %= len(COLOR_LIST)
    return COLOR_LIST[int(num)]


def draw_next_piece(screen, board, piece):
    x, y = TOP_LEFT[0] // 4, GAME_SIZE[1] // 2
    col, row = board.col, board.row
    for c, r in piece.get_cells():
        pygame.draw.rect(screen, get_color(piece.color),
                         (x + c * CELL_SIZE + 1,
                          y + r * CELL_SIZE + 1,
                          CELL_SIZE - 1,
                          CELL_SIZE - 1)
                         )
    pygame.display.update()


def draw_board(screen, board, piece):
    x, y = TOP_LEFT
    col, row = board.col, board.row
    for i in range(col + 1):
        pygame.draw.line(screen, GREY,
                         (x + i * CELL_SIZE, y),
                         (x + i * CELL_SIZE, y + GAME_SIZE[1]),
                         1 if i != 0 and i != col else 3)
    for i in range(row + 1):
        pygame.draw.line(screen, GREY,
                         (x, y + i * CELL_SIZE),
                         (x + GAME_SIZE[0], y + i * CELL_SIZE),
                         1 if i != 0 and i != row else 3)

    # board.board[1][8] = 2
    for r in range(row):
        for c in range(col):
            if board.board[r][c] != 0:
                pygame.draw.rect(screen, get_color(board.board[r][c]),
                                 (x + c * CELL_SIZE + 1,
                                  y + r * CELL_SIZE + 1,
                                  CELL_SIZE - 1,
                                  CELL_SIZE - 1)
                                 )

    for c, r in piece.get_cells():
        if 0 <= r < row and 0 <= c < col and board.board[r][c] == 0:
            pygame.draw.rect(screen, get_color(piece.color),
                             (x + c * CELL_SIZE + 1,
                              y + r * CELL_SIZE + 1,
                              CELL_SIZE - 1,
                              CELL_SIZE - 1)
                             )
    pygame.display.update()


def draw_screen(screen, board, current_piece, small_board, next_piece, score):
    screen.fill(BLACK)
    font = pygame.font.SysFont('monospace', CELL_SIZE * 2)
    label = font.render("Tetris", True, WHITE)
    screen.blit(label, (CELL_SIZE * 2, CELL_SIZE * 2))

    font = pygame.font.SysFont('Arial', CELL_SIZE)
    label = font.render(f"Score: {score}", True, WHITE)
    screen.blit(label, (CELL_SIZE * 2, CELL_SIZE * 5))

    draw_board(screen, board, current_piece)
    draw_next_piece(screen, small_board, next_piece)


def game_over_message(score):
    font = pygame.font.SysFont('Arial', CELL_SIZE * 2)
    label = font.render(f"Game Over.", True, RED)
    screen.blit(label, (WIN_SIZE[0] - GAME_SIZE[0] - CELL_SIZE * 2, CELL_SIZE * 2))
    font = pygame.font.SysFont('Arial', int(CELL_SIZE * 1.5))
    label = font.render(f"You Scored: {score}", True, RED)
    screen.blit(label, (WIN_SIZE[0] - GAME_SIZE[0] - CELL_SIZE * 2, CELL_SIZE * 4))
    font = pygame.font.SysFont('Arial', CELL_SIZE)
    label = font.render(f"Press 'Enter' to restart", True, WHITE)
    screen.blit(label, (WIN_SIZE[0] - GAME_SIZE[0] - CELL_SIZE * 2, CELL_SIZE * 7))
    label = font.render(f"Press 'ESC' to quit", True, WHITE)
    screen.blit(label, (WIN_SIZE[0] - GAME_SIZE[0] - CELL_SIZE * 2, CELL_SIZE * 9))
    pygame.display.update()


screen = pygame.display.set_mode(WIN_SIZE)
board = Board(10, 20)
small_board = Board(5, 5)
current_piece = get_random_piece()
next_piece = get_random_piece()
game_over = False
lose = False
pause = False
score = 0
clock = pygame.time.Clock()
fall_time = 0
fall_speed = .5
draw_screen(screen, board, current_piece, small_board, next_piece, score)

while not game_over:
    if not lose and not pause:
        clock.tick()
        fall_time += clock.get_time()

        if fall_time > fall_speed * 1000:
            fall_time = 0
            current_piece.move(0, 1)
            if not board.valid(current_piece):
                current_piece.move(0, -1)
                board.add_piece(current_piece)
                score += board.update()
                current_piece, next_piece = next_piece, get_random_piece()
                if not board.valid(current_piece):
                    current_piece.move(0, -1)
                    print(current_piece.get_cells(), current_piece.state, current_piece.color)
                    board.print(current_piece)
                    lose = True
                    draw_board(screen, board, current_piece)
                    game_over_message(score)
                    continue
            # board.print(current_piece)
            draw_screen(screen, board, current_piece, small_board, next_piece, score)

    for event in pygame.event.get():
        if event == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True

            if event.key == pygame.K_SPACE and not lose:
                pause = not pause

            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                board = Board(10, 20)
                small_board = Board(5, 5)
                current_piece = get_random_piece()
                current_piece.move(0, -1)
                next_piece = get_random_piece()
                lose = False
                score = 0
                fall_time = 0
                clock.tick()

            if event.key == pygame.K_LEFT:
                current_piece.move(-1, 0)
                if not board.valid(current_piece):
                    current_piece.move(1, 0)

            if event.key == pygame.K_RIGHT:
                current_piece.move(1, 0)
                if not board.valid(current_piece):
                    current_piece.move(-1, 0)

            if event.key == pygame.K_UP:
                current_piece.rotate(1)
                if not board.valid(current_piece):
                    current_piece.rotate(-1)

            if event.key == pygame.K_DOWN:
                cnt = 0
                while board.valid(current_piece):
                    current_piece.move(0, 1)
                    cnt -= 1
                current_piece.move(0, max(-3, cnt))

            # board.print()

pygame.quit()
quit()
