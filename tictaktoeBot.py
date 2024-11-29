import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Hằng số
WINDOW_WIDTH, WINDOW_HEIGHT = 400, 400
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = min(WINDOW_WIDTH, WINDOW_HEIGHT) // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Màu sắc
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
WIN_LINE_COLOR = (255, 0, 0)

# Thiết lập cửa sổ
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Bảng trò chơi
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def draw_lines():
    # Đường ngang
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WINDOW_WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WINDOW_WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Đường dọc
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, WINDOW_HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, WINDOW_HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)

def check_win(player):
    # Kiểm tra các hàng
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return True, [(row, col) for col in range(BOARD_COLS)]
    # Kiểm tra các cột
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True, [(row, col) for row in range(BOARD_ROWS)]
    # Kiểm tra đường chéo chính
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        return True, [(i, i) for i in range(BOARD_ROWS)]
    # Kiểm tra đường chéo phụ
    if all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True, [(i, BOARD_COLS - 1 - i) for i in range(BOARD_ROWS)]
    return False, []

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

def minimax(depth, is_max):
    score = evaluate()
    if score == 10 or score == -10:
        return score
    if all(board[row][col] != ' ' for row in range(BOARD_ROWS) for col in range(BOARD_COLS)):
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

def make_move(row, col, player):
    if board[row][col] == ' ':
        board[row][col] = player
        return True
    return False

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
                    win, win_cells = check_win(current_player)
                    if win:
                        for row, col in win_cells:
                            pygame.draw.rect(screen, WIN_LINE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
                        pygame.display.update()
                        print(f"Player {current_player} wins!")
                        pygame.time.wait(2000)
                        game_over = True
                    current_player = 'O' if current_player == 'X' else 'X'
                    draw_figures()
                    if current_player == 'O' and not game_over:
                        row, col = find_best_move()
                        make_move(row, col, current_player)
                        print("Computer's move:")
                        draw_figures()
                        win, win_cells = check_win(current_player)
                        if win:
                            for row, col in win_cells:
                                pygame.draw.rect(screen, WIN_LINE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
                            pygame.display.update()
                            print(f"Computer (O) wins!")
                            pygame.time.wait(2000)
                            game_over = True
                        current_player = 'X'
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
