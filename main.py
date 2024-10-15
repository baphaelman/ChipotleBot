import chess
import random

board = chess.Board()
outcome = board.outcome()

while not outcome:
    print(board)

    # my move
    my_move = input("Enter your move: ")
    board.push_san(my_move)

    outcome = board.outcome() # resetting outcome
    if outcome:
        break

    # computer's move
    random_move = random.choice(list(board.legal_moves))
    board.push(random_move)

    outcome = board.outcome() # resetting outcome

outcome = "White" if outcome.winner == chess.WHITE else "Black"

print(f"Game over. {outcome} wins!")