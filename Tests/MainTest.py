import chess
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import main

def late_game_test() -> None:
    board = chess.Board('8/2k2r2/8/8/3Q4/2K5/8/8 w - - 0 1')
    outcome = main.playGame(board, chess.BLACK)
    main.printOutcome(outcome)

if __name__ == "__main__":
    late_game_test()