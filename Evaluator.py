import chess
from piece_weights import *

# Evaluates the position of the baord
class Evaluator:
    # METHODS
    # evaluate(chess.Board) -> int: evalutaes a given position
    # pawn_evaluation(chess.Board) -> int: hat amount to add to evaluation, considering pawnpush and pawncenter weights
    
    pawnWeight = 100
    knightWeight = 325
    bishopWeight = 325
    rookWeight = 550
    queenWeight = 1100

    evals = [pawnWeight, knightWeight, bishopWeight, rookWeight, queenWeight]

    # Simply sums the piece weights of the player's and the opponent's pieces
    @staticmethod
    def evaluate(board: chess.Board) -> int:
        eval = 0
        color = board.turn

        if color == chess.WHITE:
            my_weights = white_weights
            other_weights = black_weights
        else:
            my_weights = black_weights
            other_weights = white_weights

        for i in range(1, 6):
            curr_pieces = board.pieces(i, color)
            other_curr_pieces = board.pieces(i, not color)
            eval += len(curr_pieces) * Evaluator.evals[i - 1] # iterate through my pieces
            eval -= len(other_curr_pieces) * Evaluator.evals[i - 1] # iterate through opponent's pieces

            # consider positional value
            for piece in curr_pieces:
                eval += my_weights[i][piece]
            for other_piece in other_curr_pieces:
                eval -= other_weights[i][other_piece]
        return eval
    
    def pawn_evaluation(board: chess.Board) -> int:
        color = board.turn
        return_value = 0
        if color == chess.WHITE:
            pawn_board = white_pawn_weights
            other_pawn_board = black_pawn_weights
        else:
            pawn_board = black_pawn_weights
            other_pawn_board = white_pawn_weights

        my_pawn_pieces = board.pieces(chess.PAWN, color)
        other_pawn_pieces = board.pieces(chess.PAWN, not color)
        for pawn in my_pawn_pieces:
            return_value += pawn_board[pawn]
        
        for pawn in other_pawn_pieces:
            return_value -= other_pawn_board[pawn]
        return return_value
    
def main():
    board = chess.Board()
    print(Evaluator.evaluate(board))

def compare_fens():
    main_board = chess.Board('r1bqkbnr/pppp1ppp/n7/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1')
    print(f"main eval: {Evaluator.evaluate(main_board)}")
    test_board = chess.Board('rnbqkbnr/ppp1pppp/8/3p4/4P3/P7/1PPP1PPP/RNBQKBNR w KQkq - 0 1')
    print(f"test eval: {Evaluator.evaluate(test_board)}")

def evaluate_fens():
    b = chess.Board('r1bqkbnr/p1pp1ppp/p7/4N3/4P3/8/PPPP1PPP/RNBQK2R w KQkq - 0 1')
    print(Evaluator.evaluate(b))
    c = chess.Board('r1b1kbnr/ppppqppp/n7/4N3/3PP3/8/PPP2PPP/RNBQKB1R w KQkq - 0 1')
    print(Evaluator.evaluate(c))

if __name__ == "__main__":
    evaluate_fens()