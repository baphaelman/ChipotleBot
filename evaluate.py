import chess

# Evaluates the position of the baord
class Evaluator:
    pawnWeight = 100
    knightWeight = 300
    bishopWeight = 300
    rookWeight = 500
    queenWeight = 900

    evals = [pawnWeight, knightWeight, bishopWeight, rookWeight, queenWeight]

    # Simply sums the piece weights of the player's and the opponent's pieces
    def evaluate(color: chess.Color, board: chess.Board) -> int:
        eval = 0
        for i in range(1, 6):
            eval += len(board.pieces(i, color)) * Evaluator.evals[i - 1] # iterate through my pieces
            eval -= len(board.pieces(i, not color)) * Evaluator.evals[i - 1] # iterate through opponent's pieces
        return eval
    
def main():
    board = chess.Board()
    print(Evaluator.evaluate(board.turn, board))

if __name__ == "__main__":
    main()