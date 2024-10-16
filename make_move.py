from typing import Tuple
import chess
from evaluate import Evaluator 

# determines which move should be made
class MoveMaker:
    
    # implements a recursive minimax algorithm
    def make_move(board: chess.Board, depth: int) -> chess.Move:
        return MoveMaker.make_move_helper(board, depth)[0]
    
    def make_move_helper(board: chess.Board, depth: int, my_move: bool=True) -> Tuple[chess.Move, int]:
        if depth == 0 or board.is_game_over():
            return None, Evaluator.evaluate(board)
        
        best_move: chess.Move = None
        largest_eval: int = float('-inf') if my_move else float('inf') # NOT biggest. minimax, remember

        for move in board.legal_moves: # iterates through possible moves
            board.push(move)
            curr_move, curr_eval = MoveMaker.make_move_helper(board, depth - 1, not my_move)
            board.pop()

            if my_move: # i want the eval after I make my move to be as low as possible (opponent's turn)
                if not best_move or curr_eval < largest_eval:
                    largest_eval = curr_eval
                    best_move = move
            else: # if its my oppponent's turn, I want them to grant me the best position
                if not best_move or curr_eval > largest_eval:
                    largest_eval = curr_eval
                    best_move = move
        
        # print(f'best move:  {best_move}  and largest eval:  {largest_eval}')
        return best_move, largest_eval

def main():
    board = chess.Board()
    board.push_san("d4")
    board.push_san("d5")

    board.push_san("Nc3")
    board.push_san("Nh6")
    print(MoveMaker.make_move(board, 1))
    print(MoveMaker.make_move(board, 2))
    print(MoveMaker.make_move(board, 3))
    print(MoveMaker.make_move(board, 4))

def test():
    board = chess.Board()
    board.push_san("e4")
    board.push_san("d5")
    print(MoveMaker.make_move(board, 1))
    print(MoveMaker.make_move(board, 2))
    print(MoveMaker.make_move(board, 3))
    print(MoveMaker.make_move(board, 4))

if __name__ == "__main__":
    test()