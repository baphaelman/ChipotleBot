import chess
import random

def playGame(board) -> chess.Outcome:
    outcome = board.outcome()

    while not outcome:
        print(board)

        # my move
        my_move = input("Enter your move: ")
        board.push_san(my_move)

        outcome = board.outcome() # resetting outcome
        if outcome:
            return outcome

        # computer's move
        random_move = random.choice(list(board.legal_moves))
        board.push(random_move)

        outcome = board.outcome() # resetting outcome
    return outcome

def printOutcome(outcome) -> None:
    outcome = "White" if outcome.winner == chess.WHITE else "Black"
    print(f"Game over. {outcome} wins!")

def main() -> None:
    board = chess.Board()

    outcome = playGame(board)
    printOutcome(outcome)

if __name__ == "__main__":
    main()