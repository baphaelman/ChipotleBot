import chess

# Evaluates the position of the baord
class Evaluator:
    pawnWeight = 100
    knightWeight = 300
    bishopWeight = 300
    rookWeight = 500
    queenWeight = 900

    evals = [pawnWeight, knightWeight, bishopWeight, rookWeight, queenWeight]

    pawnPushWeight = 25

    # Simply sums the piece weights of the player's and the opponent's pieces
    @staticmethod
    def evaluate(board: chess.Board) -> int:
        eval = 0
        color = board.turn

        for i in range(1, 6):
            eval += len(board.pieces(i, color)) * Evaluator.evals[i - 1] # iterate through my pieces
            eval -= len(board.pieces(i, not color)) * Evaluator.evals[i - 1] # iterate through opponent's pieces
        pawn_pieces = board.pieces(chess.PAWN, color)
        for pawn in pawn_pieces:
            pawn = pawn_pieces.pop()
            if color == chess.WHITE:
                value = (chess.square_rank(pawn) - 2) * Evaluator.pawnPushWeight
            else:
                value = (7 - chess.square_rank(pawn)) * Evaluator.pawnPushWeight
            eval += value
        return eval
    
    # doesn't discriminate; positions favoring black are negated
    @staticmethod
    def univ_evaluate(board: chess.Board) -> int:
        eval = 0
        for i in range(1, 6):
            eval += len(board.pieces(i, chess.WHITE)) * Evaluator.evals[i - 1] # iterate through white pieces
            eval -= len(board.pieces(i, chess.BLACK)) * Evaluator.evals[i - 1] # iterate through black pieces
        return eval
    
def main():
    board = chess.Board()
    print(Evaluator.evaluate(board))

if __name__ == "__main__":
    main()