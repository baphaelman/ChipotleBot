from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
from .MoveMaker import MoveMaker
from typing import Tuple

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5001", "https://chipotlebot.onrender.com/"]}})
board = chess.Board()
moves = [] # to search through openings
move_maker = MoveMaker()
evals = []

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

    global moves
    moves = []

    global evals
    evals = [move_maker.evaluator.canonical_evaluate(board)]

    return jsonify({'board': board.fen(), 'evaluation': evals[0]})

@app.route('/make_player_move', methods=['POST'])
def make_player_move():
    global board
    move_san = request.json.get('move')

    try:
        board.push_san(move_san)
        global moves
        moves.append(move_san)

        global evals
        evals.append(move_maker.evaluator.canonical_evaluate(board))
        return jsonify({'board': board.fen(), 'move': move_san, 'evaluation': evals[-1]})
    except (chess.IllegalMoveError, chess.InvalidMoveError):
        return jsonify({'error': 'Invalid move'}), 400

@app.route('/make_player_move_dragging', methods=['POST'])
def make_player_move_dragging():
    global board
    global board_states
    global curr_board_index
    if curr_board_index < len(board_states) - 1:
        raise Exception("Cannot make a move while not on current board state")
    
    # PAWN PROMOTION UCI MANIPULATION HERE
    move_uci = request.json.get('move')
    if board.piece_at(chess.SQUARE_NAMES.index(move_uci[:2])) is chess.PAWN and move_uci[2] in ['1', '7']:
        move_uci += 'q'
    print(move_uci)
        
    try:
        move = chess.Move.from_uci(move_uci)
        if move not in board.legal_moves:
            raise chess.IllegalMoveError(f"Illegal move: {move_uci}")
        move_san = board.san(move)
        highlighted = [chess.SQUARE_NAMES[move.from_square], chess.SQUARE_NAMES[move.to_square]]
        board.push(move)
        board_states.append(board.copy())
        curr_board_index += 1

        global moves
        moves.append(move_san)

        global evals
        evals.append(move_maker.evaluator.canonical_evaluate(board))
        return jsonify({'board': board.fen(), 'move': move_san, 'highlighted': highlighted, 'evaluation': evals[-1]})
    except (chess.IllegalMoveError, chess.InvalidMoveError):
        return jsonify({'error': 'Invalid move'}), 400

@app.route('/make_computer_move', methods=['POST'])
def make_computer_move():
    global board
    global board_states
    global curr_board_index
    global moves
    global move_maker

    move = move_maker.make_move(board, moves)
    highlighted = [chess.SQUARE_NAMES[move.from_square], chess.SQUARE_NAMES[move.to_square]]
    move_san = board.san(move)
    
    moves.append(move_san)

    board.push(move)
    board_states.append(board.copy())
    curr_board_index += 1
    outcome = board.outcome()

    global evals
    evals.append(move_maker.evaluator.canonical_evaluate(board))
    print(evals[-1])
    return jsonify({'board': board.fen(), 'move_san': move_san, 'outcome': outcome, 'highlighted': highlighted, 'evaluation': evals[-1]})

@app.route('/prev_board', methods=['POST'])
def prev_board():
    global board
    global board_states
    global curr_board_index
    global evals
    if curr_board_index > 0:
        curr_board_index -= 1
        board = board_states[curr_board_index]
    else:
        raise Exception("Cannot go to previous board state")
    print('THIS THIS THIS', evals, curr_board_index)
    return jsonify({'board': board.fen(), 'evaluation': evals[curr_board_index]})

@app.route('/next_board', methods=['POST'])
def next_board():
    global board
    global board_states
    global curr_board_index
    global evals
    if curr_board_index < len(board_states) - 1:
        curr_board_index += 1
        board = board_states[curr_board_index]
    else:
        raise Exception("Cannot go to next board state")
    print('THIS THIS THIS', evals, curr_board_index)
    return jsonify({'board': board.fen(), 'evaluation': evals[curr_board_index]})

@app.route('/undo', methods=['POST'])
def undo():
    global board
    global board_states
    global curr_board_index
    
    if curr_board_index < len(board_states) - 1:
        raise Exception("Cannot make a move while not on current board state")
    
    global moves
    moves.pop()
    moves.pop()

    global evals
    evals.pop()
    evals.pop()

    board.pop()
    board.pop()
    board_states.pop()
    board_states.pop()
    curr_board_index -= 2
    return jsonify({'board': board.fen(), 'evaluation': evals[-1]})

@app.route('/get_board', methods=['GET'])
def get_board():
    global board
    global evals
    return jsonify({'board': board.fen(), 'evaluation': evals[-1]})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)