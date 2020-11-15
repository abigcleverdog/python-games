import numpy as np
import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COL_COUNT = 7
CELL_SIZE = 50
RADIUS = CELL_SIZE // 2 - 5
WIDTH = COL_COUNT * CELL_SIZE
HEIGHT = int((ROW_COUNT + 1.5) * CELL_SIZE)

MYFONT = pygame.font.SysFont('monospace', CELL_SIZE//3)


def create_board():
    return np.zeros((ROW_COUNT, COL_COUNT))


def drop_piece(board, col, piece):
    row = get_next_open_row(board, col)
    board[row][col] = piece


def is_valid_location(board, column):
    return board[ROW_COUNT - 1][column] == 0


def get_next_open_row(board, column):
    for i in range(ROW_COUNT):
        if board[i][column] == 0:
            return i


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, column):
    for row in range(ROW_COUNT - 1, -1, -1):
        if board[row][column] != 0:
            break
    piece = board[row][column]
    left = right = column
    while left >= 0 and board[row][left] == piece:
        left -= 1
    while right < COL_COUNT and board[row][right] == piece:
        right += 1
    if right - left > 4:
        return True
    left = right = row
    while left >= 0 and board[left][column] == piece:
        left -= 1
    while right < ROW_COUNT and board[right][column] == piece:
        right += 1
    if right - left > 4:
        return True
    left = right = 0
    while row - left >= 0 and column - left >= 0 and board[row - left][column - left] == piece:
        left += 1
    while row + right < ROW_COUNT and column + right < COL_COUNT and board[row + right][column + right] == piece:
        right += 1
    if left + right > 4:
        return True
    left = right = 0
    while row + left < ROW_COUNT and column - left >= 0 and board[row + left][column - left] == piece:
        left += 1
    while row - right >= 0 and column + right < COL_COUNT and board[row - right][column + right] == piece:
        right += 1
    if left + right > 4:
        return True
    return False


def get_column(p):
    while True:
        try:
            col = int(input(f"Player {p} Make your Selection (0-6):"))
            if col < 0 or col > 6:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a number within [0-6]")
    return col


def draw_board(screen, board):
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (0, int(CELL_SIZE * 1.5), CELL_SIZE * COL_COUNT, CELL_SIZE * ROW_COUNT))
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                color = RED
            elif board[r][c] == 2:
                color = YELLOW
            else:
                color = BLACK
            pygame.draw.circle(screen, color, (c * CELL_SIZE + CELL_SIZE // 2, (r + 2) * CELL_SIZE),
                               RADIUS)
        pygame.display.update()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
board = create_board()
draw_board(screen, board)

game_over = False
won = False
turn = 0

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True

            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER and won:
                won = False
                board = create_board()
                draw_board(screen, board)

        if won:
            continue

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, CELL_SIZE//2, WIDTH, CELL_SIZE))
            x, y = event.pos
            x //= CELL_SIZE
            color = RED if turn == 0 else YELLOW
            pygame.draw.circle(screen, color, (x * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, CELL_SIZE//2, WIDTH, CELL_SIZE))
            x, y = event.pos
            column = x // CELL_SIZE
            if is_valid_location(board, column):
                drop_piece(board, column, 1 if turn == 0 else 2)
                print_board(board)
                draw_board(screen, np.flip(board, 0))
            else:
                continue

            if winning_move(board, column):
                print(f"Player {turn + 1} wins!!! Congratulations!!!")
                label = MYFONT.render(f"Player {turn + 1} wins!!!",
                                      True,
                                      RED if turn == 0 else YELLOW)
                screen.blit(label, (CELL_SIZE*2, CELL_SIZE//3))
                label = MYFONT.render("Press 'Enter' to restart",
                                      True,
                                      RED if turn == 0 else YELLOW,
                                      WHITE if turn == 0 else None)
                screen.blit(label, (CELL_SIZE, CELL_SIZE//3 * 3))
                pygame.display.update()
                won = True

            turn ^= 1

pygame.quit()
quit()
