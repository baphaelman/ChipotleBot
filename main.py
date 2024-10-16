import chess
from MoveMaker import MoveMaker

def playGame() -> chess.Outcome:
    board = chess.Board()
    outcome = None

    while not outcome:
        print()
        print(board)
        # my move
        my_move = input("Enter your move: ")
        board.push_san(my_move)

        if board.outcome():
            outcome = board.outcome()
            break
        
        # computer's move
        outcome = playTurn(board)

    return outcome

def playTurn(board) -> chess.Outcome:
    move = MoveMaker.make_move(board, 3)
    board.push(move)

    return board.outcome()

def printOutcome(outcome) -> None:
    outcome = "White" if outcome.winner == chess.WHITE else "Black"
    print(f"Game over. {outcome} wins!")


def main() -> None:
    outcome = playGame()
    printOutcome(outcome)

if __name__ == "__main__":
    main()