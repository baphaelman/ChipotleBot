import chess
from Evaluator import Evaluator
import random

# determines which move should be made
class MoveMaker:
    # depth_function(int) -> int: given the number of pieces on the board, determines at what depth the minimax algorithm should search
    # make_move(chess.BitBoard) -> chess.Move: given a board, returns the best move to make, kickstarts search
    # search(int, chess.Board) -> int: recursive function that implements the minimax algorithm

    num_searched = 0

    def __init__(self):
        self.evaluator = Evaluator()

    def depth_function(self, num_pieces: int) -> int:
        return int((-0.06 * num_pieces) + 5.95)
    
    def depth_function_moves(self, num_moves: int) -> int:
        return int(round(((0.0013 * num_moves ** 2) - (0.104 * num_moves) + 5.88)))
    
    def make_move(self, board: chess.Board, moves: list) -> chess.Move:
        # num_pieces = len(board.piece_map())
        # depth = MoveMaker.depth_function(num_pieces)
        num_moves = len(list(board.legal_moves))
        depth = self.depth_function_moves(num_moves)
        # print(f'num moves: {num_moves}')
        print(f'depth searched: {depth}')

        color = board.turn

        alpha = float('-inf')
        beta = float('-inf')
        
        best_move = None
        best_eval = float('-inf')

        if len(moves) < 123456789:
            moves_str = ' '.join(moves)
            if moves_str in self.evaluator.openings_dict:
                next_moves = self.evaluator.openings_dict[moves_str]
                next_move = random.choice(next_moves)
                next_next_move = random.choice(next_moves)

                # this seems convoluted but I needed to translate the san into a chess.Move lolll
                board.push_san(next_move)
                return board.pop()
            else:
                print('not in openings')

        for move in board.legal_moves:
            if not best_move:
                best_move = move
            
            board.push(move)
            eval = -1 * self.search(depth - 1, board, alpha, beta)
            if eval > best_eval:
                best_eval = eval
                best_move = move
            board.pop()

            if color == chess.WHITE:
                alpha = max(alpha, eval)
                if -1 * beta <= alpha:
                    break
            else:
                beta = max(beta, eval)
                if -1 * alpha <= beta:
                    break
        
        # print(f'alpha number searched: {MoveMaker.num_searched}')
        self.num_searched = 0
        return best_move

    def search(self, depth: int, board: chess.Board, alpha: int, beta: int) -> int:
        # base cases
        if board.is_game_over():
            self.num_searched += 1
            return float('-inf')
        if depth == 0:
            self.num_searched += 1
            return self.evaluator.evaluate(board)
        
        color = board.turn
        
        most_significant_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = -1 * self.search(depth - 1, board, alpha, beta)
            most_significant_eval = max(most_significant_eval, eval)
            board.pop()

            # overly complicated alpha beta pruning because evaluate is color-dependent
            if color == chess.WHITE:
                alpha = max(alpha, eval)
                if -1 * beta <= alpha:
                    break
            else:
                beta = max(beta, eval)
                if -1 * alpha <= beta:
                    break
        return most_significant_eval