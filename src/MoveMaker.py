import chess
import time
from Evaluator import Evaluator
import random

# determines which move should be made
class MoveMaker:
    # depth_function(int) -> int: given the number of pieces on the board, determines at what depth the minimax algorithm should search
    # make_move(chess.BitBoard) -> chess.Move: given a board, returns the best move to make, kickstarts search
    # search(int, chess.Board) -> int: recursive function that implements the minimax algorithm

    def __init__(self):
        self.evaluator = Evaluator()
        self.num_searched = 0
        self.num_quiesced = 0
        self.longest_search = []
        self.time_limit = 10000000

    def depth_function(self, num_pieces: int) -> int:
        return int((-0.06 * num_pieces) + 5.95)
    
    def depth_function_moves(self, num_moves: int) -> int:
        return int(round(((0.0013 * num_moves ** 2) - (0.104 * num_moves) + 5.88)))
    
    def make_move(self, board: chess.Board, moves: list) -> chess.Move:
        # num_pieces = len(board.piece_map())
        # depth = MoveMaker.depth_function(num_pieces)
        num_moves = len(list(board.legal_moves))
        depth = min(self.depth_function_moves(num_moves), 5)
        # print(f'num moves: {num_moves}')
        print(f'depth searched: {depth}')

        color = board.turn

        alpha = float('-inf')
        beta = float('-inf')
        
        best_move = None
        best_eval = float('-inf')

        if len(moves) <= 36: # 36 moves is the longest set of moves in the openigns dictionary
            moves_str = ' '.join(moves)
            if moves_str in self.evaluator.openings_dict:
                next_moves = self.evaluator.openings_dict[moves_str]
                next_move = random.choice(next_moves)

                # this seems convoluted but I needed to translate the san into a chess.Move lolll
                board.push_san(next_move)
                return board.pop()
            else:
                print('not in openings')

        move_count = board.legal_moves.count()
        i = 0

        # order moves by most significant
        ordered_moves = self.order_moves(list(board.legal_moves), board)
        num_moves = len(ordered_moves)
        time_per_move = self.time_limit / num_moves

        for move in ordered_moves:
            print(f'completed {i}/{move_count} of search')
            i += 1
            if not best_move:
                best_move = move
            
            board.push(move)
            move_start_time = time.time()
            eval = -1 * self.search(depth - 1, board, alpha, beta, 0, [move.uci()], move_start_time, time_per_move)
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
        print(f'quiescence count: {self.num_quiesced}')
        # print(f'fen: {board.fen()}')
        print(f'longest search: {self.longest_search} {len(self.longest_search)}')
        self.num_searched = 0
        return best_move

    def search(self, depth: int, board: chess.Board, alpha: int, beta: int, extensions: int, moves_tracker: list, start_time, time_limit) -> int:
        # base cases
        if board.is_game_over():
            self.num_searched += 1
            if board.is_checkmate():
                return float('-inf') if board.turn == chess.WHITE else float('inf')
            return 0
        if depth == 0:
            self.num_searched += 1

            # quiescence count and lists
            if extensions > self.num_quiesced:
                self.num_quiesced = extensions
            if len(moves_tracker) > len(self.longest_search):
                self.longest_search = moves_tracker
            return self.evaluator.evaluate(board)
        
        color = board.turn
        
        most_significant_eval = float('-inf')

        # order moves by most significant
        ordered_moves = self.order_moves(list(board.legal_moves), board)
        for move in ordered_moves:
            if time.time() - start_time >= time_limit: # timeout
                print('timeout', move)
                return alpha

            # quiescent search
            quiesce = self.is_quiescent_move(depth, move, board) and extensions < 6
            # quiesce = False # CHANGE THIS BACK
            # CHANGE THAT BACK
            # CHANGE THAT BACK
            # CHANGE THAT BACK
            # CHANGE THAT BACK
            # CHANGE THAT BACK
            # CHANGE THAT BACK

            new_moves_tracker = moves_tracker.copy()
            new_moves_tracker.append(move.uci())
            
            board.push(move)
            
            if quiesce:
                # print('quiescing', extensions + 1)
                eval = -1 * self.search(depth, board, alpha, beta, extensions + 1, new_moves_tracker, start_time, time_limit)
            else:
                eval = -1 * self.search(depth - 1, board, alpha, beta, extensions, new_moves_tracker, start_time, time_limit)
            if type(eval) == str:
                return eval
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
    
    def is_quiescent_move(self, depth: int, move: chess.Move, board: chess.Board) -> bool:
        return depth == 1 and (board.is_capture(move) or board.gives_check(move))
    
    def order_moves(self, moves: list[chess.Move], board: chess.Board) -> list[chess.Move]:
        move_to_score = {}
        for move in moves:
            move_score = 0
            start_piece_weight = Evaluator.start_weight_from_move(board, move)
            if board.is_capture(move):
                # print('first test:', board.piece_type_at(move.to_square))
                if board.piece_type_at(move.to_square) == None:  # if en passant basically
                    capture_piece_weight = Evaluator.evals[0]
                else:
                    capture_piece_weight = Evaluator.string_to_weight[Evaluator.piece_to_string[board.piece_type_at(move.to_square)]]
            else:
                capture_piece_weight = 0

            # their weight - our weight
            if capture_piece_weight != 0: # if piece was even captured
                move_score -= start_piece_weight
                move_score += capture_piece_weight
            
            # checking
            if board.gives_check(move):
                move_score += 3

            # promoting a pawn
            if board.piece_at(move.from_square) == chess.PAWN and move.to_square in [0, 1, 2, 3, 4, 5, 6, 7,
                                                                                     56, 57, 58, 59, 60, 61, 62, 63]:
                move_score += 10

            # don't move piece to a square a pawn can attack
            if self.is_square_attacked_by_pawn(board, move.to_square, not board.turn):
                move_score -= 5

            move_to_score[move] = move_score
        return sorted(moves, key=lambda move: move_to_score[move], reverse=True)
    
    def is_square_attacked_by_pawn(self, board: chess.Board, square: int, color: chess.Color) -> bool:
        attackers = board.attackers(color, square)
        for attacker in attackers:
            if board.piece_type_at(attacker) == chess.PAWN:
                return True
        return False