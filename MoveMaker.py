import chess
from Evaluator import Evaluator 

# determines which move should be made
class MoveMaker:

    # implements minimax recursive algorithm
    def make_move(board: chess.Board, depth: int):
        best_move = None
        best_eval = float('-inf')

        for move in board.legal_moves:
            board.push(move)
            eval = -1 * MoveMaker.search(depth - 1, board)
            if eval > best_eval:
                best_eval = eval
                best_move = move
            board.pop()

        return best_move
    
    def search(depth: int, board: chess.Board) -> int:
        # base cases
        if board.is_game_over():
            return float('-inf')
        if depth == 0:
            return Evaluator.evaluate(board)
        

        most_significant_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            most_significant_eval = max(most_significant_eval, -1 * MoveMaker.search(depth - 1, board))
            board.pop()
        return most_significant_eval


def main():
    board = chess.Board()
    board.push_san("e4")
    board.push_san("e5")

    board.push_san("Nf3")
    board.push_san("Na6")
    print(MoveMaker.make_move(board, 1))
    print(MoveMaker.make_move(board, 3))
    print(MoveMaker.make_move(board, 2))
    print(MoveMaker.make_move(board, 4))

def test():
    board = chess.Board()
    board.push_san("e4")
    board.push_san("d5")
    board.push_san("a3")
    print(MoveMaker.make_move(board, 1))
    print(MoveMaker.make_move(board, 2))
    print(MoveMaker.make_move(board, 3))
    print(MoveMaker.make_move(board, 4))

if __name__ == "__main__":
    print('test:')
    test()

    print('main:')
    main()