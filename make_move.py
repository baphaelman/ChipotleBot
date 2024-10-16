from typing import Tuple, Dict
import chess
from evaluate import Evaluator 

# determines which move should be made
class MoveMaker:
    
    # implements a recursive minimax algorithm
    def make_move(board: chess.Board, depth: int) -> chess.Move:
        return MoveMaker.make_move_helper(board, depth)[0]
    
    def make_move_helper(board: chess.Board, depth: int, my_move: bool=True) -> Tuple[chess.Move, int]:
        if depth == 0 or board.is_game_over():
            return None, Evaluator.univ_evaluate(board)
        
        moves_dict: Dict[int, chess.Move]  = {} # seems weird, but because key search is faster (right?)

        for move in board.legal_moves: # iterates through possible moves
            board.push(move)
            _, curr_eval = MoveMaker.make_move_helper(board, depth - 1, not my_move)
            board.pop()

            moves_dict[curr_eval] = move
        
        # print(f'moves depth {depth}: {moves_dict}')
        if my_move:
            most_significant_eval = max(moves_dict)
            best_move = moves_dict[most_significant_eval]
        else:
            most_significant_eval = min(moves_dict)
            best_move = moves_dict[most_significant_eval]
        
        return best_move, most_significant_eval

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
    board.push_san("d4")
    board.push_san("a5")
    board.push_san("e4")
    board.push_san("Ra6")
    print(MoveMaker.make_move(board, 1))
    print(MoveMaker.make_move(board, 2))
    print(MoveMaker.make_move(board, 3))
    print(MoveMaker.make_move(board, 4))

if __name__ == "__main__":
    test()