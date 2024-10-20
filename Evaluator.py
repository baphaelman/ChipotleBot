import chess

# Evaluates the position of the baord
class Evaluator:
    pawnWeight = 100
    knightWeight = 300
    bishopWeight = 300
    rookWeight = 500
    queenWeight = 900

    evals = [pawnWeight, knightWeight, bishopWeight, rookWeight, queenWeight]

    pawnPushWeight = 10
    pawnCenterWeight = 10

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

    
    # doesn't discriminate; positions favoring black are negated
    @staticmethod
    def univ_evaluate(board: chess.Board) -> int:
        eval = 0
        for i in range(1, 6):
            eval += len(board.pieces(i, chess.WHITE)) * Evaluator.evals[i - 1] # iterate through white pieces
            eval -= len(board.pieces(i, chess.BLACK)) * Evaluator.evals[i - 1] # iterate through black pieces
        return eval
    
    def pawn_evaluation(board: chess.Board) -> int:
        color = board.turn
        return_value = 0

        my_pawn_pieces = board.pieces(chess.PAWN, color)
        other_pawn_pieces = board.pieces(chess.PAWN, not color)
        for pawn in my_pawn_pieces:
            pawn_rank = chess.square_rank(pawn)
            pawn_file = chess.square_file(pawn)
            if color == chess.WHITE:
                return_value += (pawn_rank - 1) * Evaluator.pawnPushWeight
                return_value += max(abs(pawn_file - 3), abs(pawn_file - 4)) * Evaluator.pawnCenterWeight
            else:
                return_value += (6 - pawn_rank) * Evaluator.pawnPushWeight
                return_value += max(abs(pawn_file - 3), abs(pawn_file - 4)) * Evaluator.pawnCenterWeight
        
        for pawn in other_pawn_pieces:
            pawn_rank = chess.square_rank(pawn)
            pawn_file = chess.square_file(pawn)
            if color == chess.WHITE:
                return_value -= (6 - pawn_rank) * Evaluator.pawnPushWeight
                return_value += max(abs(pawn_file - 3), abs(pawn_file - 4)) * Evaluator.pawnCenterWeight
            else:
                return_value -= (pawn_rank - 2) * Evaluator.pawnPushWeight
                return_value += max(abs(pawn_file - 3), abs(pawn_file - 4)) * Evaluator.pawnCenterWeigh
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