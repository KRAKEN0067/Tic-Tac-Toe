from flask import Flask, render_template, jsonify, request, session
from tictactoe_ai import find_best_move, check_winner # Import your AI functions

app = Flask(__name__)
# A secret key is required for sessions to work
app.secret_key = 'your_secret_key' 

@app.route('/')
def index():
    """Renders the main game page and initializes the board in the session."""
    session['board'] = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    """Handles a player's move and triggers the AI's response."""
    data = request.json
    board = session.get('board')
    
    # Player's move
    player_row, player_col = data['row'], data['col']
    if board[player_row][player_col] == ' ':
        board[player_row][player_col] = 'O'
    else:
        # Invalid move
        return jsonify({'status': 'error', 'message': 'Invalid move'}), 400

    # Check for winner after player's move
    winner = check_winner(board)
    if winner:
        session['board'] = board
        return jsonify({'status': 'game_over', 'winner': winner, 'board': board})

    # AI's move
    ai_move = find_best_move(board)
    if ai_move:
        board[ai_move[0]][ai_move[1]] = 'X'
    
    # Check for winner after AI's move
    winner = check_winner(board)
    
    # Update the session board
    session['board'] = board
    
    if winner:
        return jsonify({'status': 'game_over', 'winner': winner, 'board': board})
    else:
        return jsonify({'status': 'success', 'board': board})

@app.route('/reset', methods=['POST'])
def reset():
    """Resets the game board."""
    session['board'] = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]
    return jsonify({'status': 'success', 'board': session.get('board')})

if __name__ == '__main__':
    app.run(debug=True)