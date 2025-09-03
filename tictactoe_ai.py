import math

# --- 1. Game Foundation ---

def print_board(board):
    """Prints the Tic-Tac-Toe board."""
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
    print("\n")

def get_available_moves(board):
    """Returns a list of available moves (row, col)."""
    moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                moves.append((row, col))
    return moves

def make_move(board, row, col, player):
    """Makes a move on the board if the spot is available."""
    if board[row][col] == ' ':
        board[row][col] = player
        return True
    return False

def check_winner(board):
    """
    Checks for a winner, a tie, or if the game is ongoing.
    Returns 'X', 'O', 'Tie', or None.
    """
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != ' ':
            return board[row][0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]

    # Check for a tie
    if not any(' ' in row for row in board):
        return 'Tie'

    return None

# --- 2. AI Logic (Minimax with Alpha-Beta Pruning) ---

scores = {'X': 1, 'O': -1, 'Tie': 0}

def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Minimax algorithm with Alpha-Beta Pruning.
    """
    result = check_winner(board)
    if result is not None:
        return scores[result]

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(board):
            row, col = move
            make_move(board, row, col, 'X')
            score = minimax(board, depth + 1, False, alpha, beta)
            board[row][col] = ' ' # Undo the move
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves(board):
            row, col = move
            make_move(board, row, col, 'O')
            score = minimax(board, depth + 1, True, alpha, beta)
            board[row][col] = ' ' # Undo the move
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        return best_score

def find_best_move(board):
    """
    Finds the best move for the AI player 'X'.
    """
    best_move = None
    best_score = -math.inf
    for move in get_available_moves(board):
        row, col = move
        make_move(board, row, col, 'X')
        move_score = minimax(board, 0, False, -math.inf, math.inf)
        board[row][col] = ' ' # Undo the move
        if move_score > best_score:
            best_score = move_score
            best_move = move
    return best_move

# --- 3. Main Game Loop ---

def main():
    board = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]
    print("Welcome to AI Tic-Tac-Toe!")
    print("You are 'O'. The AI is 'X'.")

    while True:
        print_board(board)
        winner = check_winner(board)
        if winner:
            if winner == 'Tie':
                print("It's a Tie!")
            else:
                print(f"Player {winner} wins!")
            break

        # Human player's turn
        try:
            row, col = map(int, input("Enter your move (row col): ").split())
            if not make_move(board, row, col, 'O'):
                print("Invalid move. Spot already taken. Try again.")
                continue
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column as two numbers (e.g., 0 1).")
            continue
        
        # Check for winner after human move
        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == 'Tie':
                print("It's a Tie!")
            else:
                print(f"Player {winner} wins!")
            break

        # AI player's turn
        print("AI is thinking...")
        ai_move = find_best_move(board)
        if ai_move:
            make_move(board, ai_move[0], ai_move[1], 'X')

if __name__ == "__main__":
    main()