import streamlit as st
import numpy as np
import time  # Thêm để tạo hiệu ứng tính toán

# Constants
PLAYER = "X"  # Human
BOT = "O"  # AI

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = np.full((3, 3), "")  # Empty board
    st.session_state.current_player = PLAYER
    st.session_state.winner = None
    st.session_state.bot_calculating = False  # Trạng thái bot đang tính toán

# Check winner
def check_winner(board):
    # Rows, columns, and diagonals
    lines = [
        board[i, :] for i in range(3)
    ] + [board[:, i] for i in range(3)] + [board.diagonal(), np.fliplr(board).diagonal()]
    for line in lines:
        if len(set(line)) == 1 and line[0] != "":
            return line[0]
    if "" not in board:
        return "Draw"
    return None

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == BOT:
        return 1
    elif winner == PLAYER:
        return -1
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i, j] == "":
                    board[i, j] = BOT
                    score = minimax(board, depth + 1, False)
                    board[i, j] = ""
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i, j] == "":
                    board[i, j] = PLAYER
                    score = minimax(board, depth + 1, True)
                    board[i, j] = ""
                    best_score = min(best_score, score)
        return best_score

# Bot's move
def bot_move():
    st.session_state.bot_calculating = True  # Bật trạng thái "đang tính toán"
    time.sleep(1)  # Hiệu ứng tính toán
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if st.session_state.board[i, j] == "":
                st.session_state.board[i, j] = BOT
                score = minimax(st.session_state.board, 0, False)
                st.session_state.board[i, j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        st.session_state.board[move] = BOT
    st.session_state.bot_calculating = False  # Tắt trạng thái "đang tính toán"

# Game logic
def play_turn(row, col):
    if st.session_state.board[row, col] == "" and not st.session_state.winner and not st.session_state.bot_calculating:
        st.session_state.board[row, col] = PLAYER
        st.session_state.winner = check_winner(st.session_state.board)
        if not st.session_state.winner:
            bot_move()
            st.session_state.winner = check_winner(st.session_state.board)

# UI rendering
st.title("Tic Tac Toe with Minimax Bot")

# Show "Bot đang tính toán" message
if st.session_state.bot_calculating:
    st.write("🤖 Bot đang tính toán...")

# Draw the board
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        with cols[j]:
            if st.button(st.session_state.board[i, j] or " ", key=f"{i}-{j}"):
                play_turn(i, j)

# Show result
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.write("🤝 It's a draw!")
    else:
        st.write(f"🎉 {st.session_state.winner} wins!")

# Reset button
if st.button("Restart"):
    st.session_state.board = np.full((3, 3), "")
    st.session_state.current_player = PLAYER
    st.session_state.winner = None
    st.session_state.bot_calculating = False
