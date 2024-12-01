from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
from MoveMaker import MoveMaker
from typing import Tuple

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})  # Allow React origin
board = chess.Board()

def playTurn(board) -> Tuple[chess.Move, chess.Outcome]:
    move = MoveMaker.make_move(board)
    board.push(move)
    return move, board.outcome()

@app.route('/')
def index():
    return "Flask server is running!"

@app.route('/start_game', methods=['POST'])
def start_game():
    global board
    board = chess.Board()

    global board_states
    board_states = [board.copy()]

    global curr_board_index
    curr_board_index = 0

    return jsonify({'board': board.fen()})

@app.route('/make_player_move', methods=['POST'])
def make_player_move():
    global board
    move_san = request.json.get('move')
    try:
        board.push_san(move_san)
        return jsonify({'board': board.fen(), 'move': move_san})
    except (chess.IllegalMoveError, chess.InvalidMoveError):
        return jsonify({'error': 'Invalid move'}), 400

@app.route('/make_player_move_dragging', methods=['POST'])
def make_player_move_dragging():
    global board
    global board_states
    global curr_board_index
    if curr_board_index < len(board_states) - 1:
        raise Exception("Cannot make a move while not on current board state")
    
    move_uci = request.json.get('move')
    try:
        move = chess.Move.from_uci(move_uci)
        if move not in board.legal_moves:
            raise chess.IllegalMoveError(f"Illegal move: {move_uci}")
        move_san = board.san(move)
        board.push(move)
        board_states.append(board.copy())
        curr_board_index += 1
        return jsonify({'board': board.fen(), 'move': move_san})
    except (chess.IllegalMoveError, chess.InvalidMoveError):
        return jsonify({'error': 'Invalid move'}), 400

@app.route('/prev_board', methods=['POST'])
def prev_board():
    global board
    global board_states
    global curr_board_index
    if curr_board_index > 0:
        curr_board_index -= 1
        board = board_states[curr_board_index]
    return jsonify({'board': board.fen()})

@app.route('/next_board', methods=['POST'])
def next_board():
    global board
    global board_states
    global curr_board_index
    if curr_board_index < len(board_states) - 1:
        curr_board_index += 1
        board = board_states[curr_board_index]
    return jsonify({'board': board.fen()})

@app.route('/make_computer_move', methods=['POST'])
def make_computer_move():
    global board
    global board_states
    global curr_board_index

    move = MoveMaker.make_move(board)
    move_san = board.san(move)
    board.push(move)
    board_states.append(board.copy())
    curr_board_index += 1
    outcome = board.outcome()
    return jsonify({'board': board.fen(), 'move_san': move_san, 'outcome': outcome})


@app.route('/get_board', methods=['GET'])
def get_board():
    global board
    return jsonify({'board': board.fen()})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)