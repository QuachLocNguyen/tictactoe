import streamlit as st
import numpy as np

# Khởi tạo bảng trò chơi
board = np.full((3, 3), ' ')

# Hàm hiển thị bảng
def display_board():
    st.write("### Tic-Tac-Toe")
    for row in board:
        st.write(' | '.join(row))
        st.write('-' * 5)

# Kiểm tra người thắng
def check_win(player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

# Đánh giá trạng thái bảng
def evaluate():
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return 10 if row[0] == 'O' else -10
    for col in range(3):
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
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    best = max(best, minimax(depth + 1, not is_max))
                    board[i][j] = ' '
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    best = min(best, minimax(depth + 1, not is_max))
                    board[i][j] = ' '
        return best

# Tìm nước đi tốt nhất cho bot
def find_best_move():
    best_val = -1000
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
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
    st.title("Tic-Tac-Toe với Bot")
    display_board()
    current_player = 'X'
    game_over = False
    
    if st.button("Reset Game"):
        global board
        board = np.full((3, 3), ' ')
        st.experimental_rerun()
    
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            if cols[j].button(f"{board[i][j]}", key=f"{i}-{j}"):
                if make_move(i, j, current_player):
                    if check_win(current_player):
                        st.write(f"Người chơi {current_player} thắng!")
                        game_over = True
                    current_player = 'O' if current_player == 'X' else 'X'
                    if current_player == 'O' and not game_over:
                        row, col = find_best_move()
                        make_move(row, col, current_player)
                        if check_win(current_player):
                            st.write(f"Người chơi {current_player} thắng!")
                            game_over = True
                        current_player = 'X'
                    st.experimental_rerun()

play_game()
