import pygame
import sys
import random

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Màu sắc
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Thiết lập cửa sổ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Bảng trò chơi
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Vẽ các đường kẻ
def draw_lines():
    # Đường ngang
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Đường dọc
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Vẽ các dấu X và O
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)

# Kiểm tra người thắng
def check_win(player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True
    if all([board[i][i] == player for i in range(BOARD_ROWS)]) or all([board[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)]):
        return True
    return False

# Đánh giá trạng thái bảng
def evaluate():
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return 10 if row[0] == 'O' else -10
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return 10 if board[0][col] == 'O' else -10
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return 10 if board[0][0] == 'O' else -10
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return 10 if board[0][2] == 'O' else -10
    return 0

# Thuật toán Minimax
def minimax(depth, is_max):
    score = evaluate()
    if score == 10 or score == -10:
        return score
    if all([cell != ' ' for row in board for cell in row]):
        return 0
    if is_max:
        best = -1000
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    best = max(best, minimax(depth + 1, not is_max))
                    board[i][j] = ' '
        return best
    else:
        best = 1000
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    best = min(best, minimax(depth + 1, not is_max))
                    board[i][j] = ' '
        return best

# Tìm nước đi tốt nhất cho bot
def find_best_move():
    best_val = -1000
    best_move = (-1, -1)
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_val = minimax(0, False)
                board[i][j] = ' '
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move

# Thực hiện nước đi
def make_move(row, col, player):
    if board[row][col] == ' ':
        board[row][col] = player
        return True
    return False

# Chơi trò chơi
def play_game():
    draw_lines()
    current_player = 'X'
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE
                if make_move(mouseY, mouseX, current_player):
                    if check_win(current_player):
                        game_over = True
                    current_player = 'O' if current_player == 'X' else 'X'
                    draw_figures()
                    if current_player == 'O' and not game_over:
                        row, col = find_best_move()
                        make_move(row, col, current_player)
                        if check_win(current_player):
                            game_over = True
                        current_player = 'X'
                        draw_figures()
            if game_over:
                pygame.time.wait(2000)
                board[:] = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
                game_over = False
                current_player = 'X'
                screen.fill(BG_COLOR)
                draw_lines()
                draw_figures()
        pygame.display.update()

play_game()
