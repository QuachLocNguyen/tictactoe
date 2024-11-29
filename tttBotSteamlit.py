import streamlit as st
import numpy as np

# Hằng số
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = 100

# Màu sắc
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
WIN_LINE_COLOR = (255, 0, 0)

# Bảng trò chơi
board = np.full((BOARD_ROWS, BOARD_COLS), ' ')

def draw_lines(canvas):
    # Đường ngang
    for i in range(1, BOARD_ROWS):
        canvas.write_text("", x=0, y=i * SQUARE_SIZE, font_size=1, color=LINE_COLOR)
    # Đường dọc
    for i in range(1, BOARD_COLS):
        canvas.write_text("", x=i * SQUARE_SIZE, y=0, font_size=1, color=LINE_COLOR)

def draw_figures(canvas):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                canvas.write_text("X", x=col * SQUARE_SIZE + SQUARE_SIZE // 4, y=row * SQUARE_SIZE + SQUARE_SIZE // 4, font_size=50, color=CROSS_COLOR)
                canvas.write_text("X", x=col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, y=row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, font_size=50, color=CROSS_COLOR)
            elif board[row][col] == 'O':
                canvas.circle(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2, SQUARE_SIZE // 3, stroke_color=CIRCLE_COLOR, stroke_width=15)

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
    st.title("Tic Tac Toe")
    canvas = st.empty()
    current_player = 'X'
    game_over = False

    while True:
        draw_lines(canvas)
        draw_figures(canvas)

        if not game_over:
            if current_player == 'X':
                clicked = canvas.button("Your turn", key="player_turn")
                if clicked:
                    mouseX, mouseY = st.session_state.get("clicked_pos", (None, None))
                    if mouseX is not None and mouseY is not None:
                        row, col = mouseY // SQUARE_SIZE, mouseX // SQUARE_SIZE
                        if make_move(row, col, current_player):
                            win, win_cells = check_win(current_player)
                            if win:
                                for row, col in win_cells:
                                    canvas.write_text("", x=col * SQUARE_SIZE, y=row * SQUARE_SIZE, font_size=1, color=WIN_LINE_COLOR)
                                st.write(f"Player {current_player} wins!")
                                game_over = True
                            current_player = 'O'
                            st.session_state.clicked_pos = None
            else:
                row, col = find_best_move()
                make_move(row, col, current_player)
                win, win_cells = check_win(current_player)
                if win:
                    for row, col in win_cells:
                        canvas.write_text("", x=col * SQUARE_SIZE, y=row * SQUARE_SIZE, font_size=1, color=WIN_LINE_COLOR)
                    st.write(f"Computer (O) wins!")
                    game_over = True
                current_player = 'X'

        if game_over:
            if st.button("Play Again"):
                board[:] = [' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)
                game_over = False
                current_player = 'X'
                canvas.empty()

        st.session_state.clicked_pos = st.experimental_get_query_params().get("clicked", (None, None))

if __name__ == "__main__":
    play_game()
