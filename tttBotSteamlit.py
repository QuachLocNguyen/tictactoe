import streamlit as st
import numpy as np

# Constants
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = 100

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
WIN_LINE_COLOR = (255, 0, 0)

def initialize_game():
    """Initialize a new game board."""
    return np.full((BOARD_ROWS, BOARD_COLS), ' ')

def draw_board(board):
    """Create a visual representation of the board using Streamlit columns."""
    cols = st.columns(BOARD_COLS)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            with cols[col]:
                cell_value = board[row][col]
                if cell_value == 'X':
                    st.markdown(f'<div style="color:{CROSS_COLOR};font-size:48px;text-align:center;">X</div>', unsafe_allow_html=True)
                elif cell_value == 'O':
                    st.markdown(f'<div style="color:{CIRCLE_COLOR};font-size:48px;text-align:center;">O</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="height:50px;"></div>', unsafe_allow_html=True)

def check_win(board, player):
    """Check if the specified player has won."""
    # Check rows and columns
    for i in range(BOARD_ROWS):
        if all(board[i, j] == player for j in range(BOARD_COLS)) or \
           all(board[j, i] == player for j in range(BOARD_ROWS)):
            return True

    # Check diagonals
    if all(board[i, i] == player for i in range(BOARD_ROWS)) or \
       all(board[i, BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True

    return False

def is_board_full(board):
    """Check if the board is completely filled."""
    return ' ' not in board

def evaluate(board):
    """Evaluate the board state for the minimax algorithm."""
    if check_win(board, 'O'):
        return 10
    elif check_win(board, 'X'):
        return -10
    return 0

def minimax(board, depth, is_maximizing):
    """Minimax algorithm with depth tracking."""
    score = evaluate(board)

    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row, col] == ' ':
                    board[row, col] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[row, col] = ' '
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row, col] == ' ':
                    board[row, col] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[row, col] = ' '
                    best_score = min(best_score, score)
        return best_score

def find_best_move(board):
    """Find the best move for the AI player."""
    best_score = float('-inf')
    best_move = None

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row, col] == ' ':
                board[row, col] = 'O'
                score = minimax(board, 0, False)
                board[row, col] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move

def play_game():
    """Main game loop implemented with Streamlit."""
    st.title("Tic Tac Toe: Human vs AI")

    # Initialize game state
    if 'board' not in st.session_state:
        st.session_state.board = initialize_game()
    if 'current_player' not in st.session_state:
        st.session_state.current_player = 'X'
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

    # Draw the current board state
    draw_board(st.session_state.board)

    # Player's turn
    if not st.session_state.game_over and st.session_state.current_player == 'X':
        row_col = st.radio("Select a cell:", 
                           [f"Row {row}, Column {col}" for row in range(BOARD_ROWS) 
                            for col in range(BOARD_COLS) 
                            if st.session_state.board[row, col] == ' '])

        if st.button("Make Move"):
            row, col = map(int, row_col.replace('Row ', '').replace(', Column ', ' ').split())
            st.session_state.board[row, col] = 'X'

            # Check for win or draw
            if check_win(st.session_state.board, 'X'):
                st.success("Congratulations! You win!")
                st.session_state.game_over = True
            elif is_board_full(st.session_state.board):
                st.warning("It's a draw!")
                st.session_state.game_over = True
            else:
                st.session_state.current_player = 'O'

    # AI's turn
    if not st.session_state.game_over and st.session_state.current_player == 'O':
        move = find_best_move(st.session_state.board)
        st.session_state.board[move] = 'O'

        # Check for win or draw
        if check_win(st.session_state.board, 'O'):
            st.error("AI wins! Better luck next time.")
            st.session_state.game_over = True
        elif is_board_full(st.session_state.board):
            st.warning("It's a draw!")
            st.session_state.game_over = True
        else:
            st.session_state.current_player = 'X'

    # Restart game option
    if st.session_state.game_over:
        if st.button("Play Again"):
            st.session_state.board = initialize_game()
            st.session_state.current_player = 'X'
            st.session_state.game_over = False
            st.experimental_rerun()

def main():
    play_game()

if __name__ == "__main__":
    main()
