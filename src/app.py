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
    return jsonify({'board': board.fen()})

# NEW STUFF
@app.route('/make_player_move', methods=['POST'])
def make_player_move():
    global board
    move_san = request.json.get('move')
    try:
        board.push_san(move_san)
        return jsonify({'board': board.fen(), 'move': move_san})
    except (chess.IllegalMoveError, chess.InvalidMoveError):
        return jsonify({'error': 'Invalid move'}), 400

@app.route('/make_computer_move', methods=['POST'])
def make_computer_move():
    global board
    move = MoveMaker.make_move(board)
    move_san = board.san(move)
    board.push(move)
    outcome = board.outcome()
    return jsonify({'board': board.fen(), 'move_san': move_san, 'outcome': outcome})


@app.route('/get_board', methods=['GET'])
def get_board():
    global board
    return jsonify({'board': board.fen()})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)