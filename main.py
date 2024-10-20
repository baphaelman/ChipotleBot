import chess
from MoveMaker import MoveMaker
from typing import Tuple

def playGame() -> chess.Outcome:
    board = chess.Board()
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
    move = MoveMaker.make_move(board, 3)
    board.push(move)

    return move, board.outcome()

def printOutcome(outcome) -> None:
    outcome = "White" if outcome.winner == chess.WHITE else "Black"
    print(f"Game over. {outcome} wins!")


def main() -> None:
    outcome = playGame()
    printOutcome(outcome)

def checkmate_test() -> None:
    board = chess.Board()
    board.push_san("e4")
    board.push_san("e5")
    board.push_san("Qh5")
    board.push_san("Nc6")
    board.push_san("Bc4")
    board.push_san("Nf6")
    board.push_san("Qxf7")
    print(board)
    print(board.outcome())

if __name__ == "__main__":
    main()