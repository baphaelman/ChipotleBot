import chess
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from Evaluator import Evaluator

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