import chess
from MoveMaker import MoveMaker
from typing import Tuple

def playGame(board: chess.Board) -> chess.Outcome:
    outcome = None
    move = None

    while not outcome:
        print(board)
        if move:
            print(f"Computer played: {move}")
        
        # my move
        retry = True
        while retry:
            my_move = input("Enter your move: ")
            if my_move == "stop":
                return outcome
            try:
                board.push_san(my_move)
                retry = False
                break
            except:
                print("Invalid move. Try again.")
                continue

        if board.outcome():
            outcome = board.outcome()
            break
        
        print()
        # computer's move
        move, outcome = playTurn(board)

    return outcome

def playTurn(board) -> Tuple[chess.Move, chess.Outcome]:
    move = MoveMaker.make_move(board)
    board.push(move)

    return move, board.outcome()

def printOutcome(outcome) -> None:
    if outcome:
        if outcome.winner == chess.WHITE:
            print("White wins!")
        elif outcome.winner == chess.BLACK:
            print("Black wins!")
        else:
            print("Draw!")
    else:
        print("Game ended prematurely.")


def main() -> None:
    board = chess.Board()
    outcome = playGame(board)
    printOutcome(outcome)

def late_game_test() -> None:
    board = chess.Board('8/2k2r2/8/8/3Q4/2K5/8/8 w - - 0 1')
    outcome = playGame(board)
    printOutcome(outcome)

if __name__ == "__main__":
    main()
    # late_game_test()