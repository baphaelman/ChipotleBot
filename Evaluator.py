import chess

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

    white_pawn_position_weights = [0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0,
                             5, 5, 10, 10, 10, 10, 5, 5,
                             15, 15, 20, 20, 20, 20, 15, 15,
                             20, 20, 30, 30, 30, 30, 20, 20,
                             30, 30, 40, 40, 40, 40, 30, 30,
                             40, 40, 50, 50, 50, 50, 40, 40,
                             0, 0, 0, 0, 0, 0, 0, 0]
    black_pawn_position_weights = list(reversed(white_pawn_position_weights))

    # Simply sums the piece weights of the player's and the opponent's pieces
    @staticmethod
    def evaluate(board: chess.Board) -> int:
        eval = 0
        color = board.turn

        for i in range(1, 6):
            eval += len(board.pieces(i, color)) * Evaluator.evals[i - 1] # iterate through my pieces
            eval -= len(board.pieces(i, not color)) * Evaluator.evals[i - 1] # iterate through opponent's pieces
        
        # add pawn positional value
        eval += Evaluator.pawn_evaluation(board)
        return eval
    
    def pawn_evaluation(board: chess.Board) -> int:
        color = board.turn
        return_value = 0
        if color == chess.WHITE:
            pawn_board = Evaluator.white_pawn_position_weights
            other_pawn_board = Evaluator.black_pawn_position_weights
        else:
            pawn_board = Evaluator.black_pawn_position_weights
            other_pawn_board = Evaluator.white_pawn_position_weights

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