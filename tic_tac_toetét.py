import streamlit as st
import numpy as np

def check_winner(board):
    # Check rows
    for row in board:
        if len(set(row)) == 1 and row[0] != ' ':
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    
    # Check for draw
    if all(cell != ' ' for row in board for cell in row):
        return 'Draw'
    
    return None

def evaluate(board):
    winner = check_winner(board)
    if winner == 'O':
        return 10
    elif winner == 'X':
        return -10
    return 0

def minimax(board, depth, is_maximizing):
    score = evaluate(board)
    
    if score == 10 or score == -10:
        return score
    
    if all(cell != ' ' for row in board for cell in row):
        return 0
    
    if is_maximizing:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    best = max(best, minimax(board, depth + 1, not is_maximizing))
                    board[i][j] = ' '
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    best = min(best, minimax(board, depth + 1, not is_maximizing))
                    board[i][j] = ' '
        return best

def find_best_move(board):
    best_val = -1000
    best_move = None
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_val = minimax(board, 0, False)
                board[i][j] = ' '
                
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    
    return best_move

def computer_move(board):
    move = find_best_move(board)
    if move:
        board[move[0]][move[1]] = 'O'
    return board

def get_board_state_emoji(board):
    emoji_board = []
    for row in board:
        emoji_row = []
        for cell in row:
            if cell == 'X':
                emoji_row.append('❌')
            elif cell == 'O':
                emoji_row.append('⭕')
            else:
                emoji_row.append('⬜')
        emoji_board.append(emoji_row)
    return emoji_board

def main():
    st.title("Tic Tac Toe with AI")

    # Initialize session state variables if not already set
    if 'board' not in st.session_state:
        st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'winner' not in st.session_state:
        st.session_state.winner = None

    board = st.session_state.board

    emoji_board = get_board_state_emoji(board)
    for row in emoji_board:
        st.write(' '.join(row))

    # Display winner message if game is over
    if st.session_state.game_over:
        if st.session_state.winner == 'X':
            st.success("You win! 🎉")
        elif st.session_state.winner == 'O':
            st.error("Computer wins! 😢")
        elif st.session_state.winner == 'Draw':
            st.warning("It's a draw! 🤝")

        # Play Again button
        if st.button("Play Again"):
            st.session_state.board = [[' ' for _ in range(3)] for _ in range(3)]
            st.session_state.game_over = False
            st.session_state.winner = None
            st.experimental_rerun()
    else:
        # Game is not over, continue playing
        col1, col2 = st.columns(2)
        with col1:
            row = st.selectbox("Select Row", [0, 1, 2], key='row_select')
        with col2:
            col = st.selectbox("Select Column", [0, 1, 2], key='col_select')

        if st.button("Make Move"):
            if board[row][col] == ' ':
                board[row][col] = 'X'
                st.session_state.board = board

                # Check if player won
                winner = check_winner(board)
                if winner == 'X':
                    st.session_state.game_over = True
                    st.session_state.winner = 'X'
                elif winner == 'Draw':
                    st.session_state.game_over = True
                    st.session_state.winner = 'Draw'
                else:
                    # Computer's move
                    board = computer_move(board)
                    st.session_state.board = board

                    # Check if computer won
                    winner = check_winner(board)
                    if winner == 'O':
                        st.session_state.game_over = True
                        st.session_state.winner = 'O'
                    elif winner == 'Draw':
                        st.session_state.game_over = True
                        st.session_state.winner = 'Draw'

if __name__ == '__main__':
    main()
