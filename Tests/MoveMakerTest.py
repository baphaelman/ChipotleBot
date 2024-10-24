import chess
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from MoveMaker import MoveMaker

class MoveMakerTest:
    def endgame_test():
        board = chess.Board('6Q1/p1p3P1/1k1p2N1/p1n1p2P/5r2/1b6/2n4K/b1q2b2 b - - 29 30')
        board2 = chess.Board('8/8/8/1Q6/8/2K5/8/k7 w - - 0 1')
        board3 = chess.Board('1Q6/8/8/8/8/2K5/k7/8 w - - 0 1')
        board4 = chess.Board('6QR/8/3p1kN1/1P5P/3N1r2/1b4P1/3r4/2K2b2 b - - 13 10')
        
        print("MOVE 1 IS: ", MoveMaker.make_move(board))
        print("MOVE 2 IS: ", MoveMaker.make_move(board2))
        print("MOVE 3 IS: ", MoveMaker.make_move(board3))
        print("MOVE 4 IS: ", MoveMaker.make_move(board4))
    
    def main():
        board = chess.Board()
        board.push_san("e4")
        board.push_san("e5")

        board.push_san("Nf3")
        board.push_san("Na6")
        print(MoveMaker.make_move(board))

    def test(): 
        board = chess.Board()
        board.push_san("e4")
        board.push_san("d5")
        board.push_san("a3")
        print(MoveMaker.make_move(board))

if __name__ == "__main__":
    MoveMakerTest.endgame_test()
    # MoveMakerTest.main()
    # MoveMakerTest.test()