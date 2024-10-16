from typing import Tuple, Dict
import chess
from Evaluator import Evaluator 

# determines which move should be made
class MoveMaker:
    
    # implements a recursive minimax algorithm
    @staticmethod
    def make_move(board: chess.Board, depth: int) -> chess.Move:
        return MoveMaker.make_move_helper(board, depth)[0]
    
    @staticmethod
    def make_move_helper(board: chess.Board, depth: int, my_move: bool=True) -> Tuple[chess.Move, int]:
        if depth == 0 or board.is_game_over():
            return None, -1 * Evaluator.univ_evaluate(board)
        
        moves_dict: Dict[chess.Move, int] = {}

        for move in board.legal_moves: # iterates through possible moves
            board.push(move)
            _, curr_eval = MoveMaker.make_move_helper(board, depth - 1, not my_move)
            board.pop()

            moves_dict[move] = curr_eval # records moves and their evaluations
        
        if my_move:
            best_move = max(moves_dict, key=moves_dict.get)
            most_significant_eval = moves_dict[best_move]
        else:
            best_move = min(moves_dict, key=moves_dict.get)
            most_significant_eval = moves_dict[best_move]
        
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
    board.push_san("e4")
    board.push_san("d5")
    board.push_san("a3")
    print(MoveMaker.make_move(board, 1))
    print(MoveMaker.make_move(board, 2))
    print(MoveMaker.make_move(board, 3))
    print(MoveMaker.make_move(board, 4))

if __name__ == "__main__":
    test()