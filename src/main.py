import chess
from MoveMaker import MoveMaker
from typing import Tuple

def playGame(board: chess.Board, player_color: chess.Color, board_states: list[chess.Board]) -> chess.Outcome:
    move_number = 0
    computer_color = not player_color
    outcome = None
    move = None

    if computer_color == chess.WHITE:
        print(board.unicode())
        print()
        move, outcome = playTurn(board)

    while not outcome:
        print(board.unicode())
        if move:
            print(f"Computer played: {move}")

        
        # my move
        retry = True
        while retry:
            my_move = input("Enter your move: ")
            if my_move == "stop":
                return outcome
            elif my_move == "undo":
                board.pop()
                board.pop()
                print(board.unicode())
                continue
            try:
                board.push_san(my_move)
                board_states.append(board.copy())
                move_number += 1
                retry = False
                break
            except (chess.IllegalMoveError, chess.InvalidMoveError):
                print("Invalid move. Try again.")
                continue

        if board.outcome():
            outcome = board.outcome()
            break

        print()
        
        # computer's move
        move, outcome, san = playTurn(board)
        move_number += 1
    
    if outcome.winner == computer_color: # show final board if computer wins on their move
        print(board.unicode())
    
    return outcome

def playTurn(board):
    move = MoveMaker.make_move(board)
    move_san = board.san(move)
    board.push(move)
    return move, board.outcome(), move_san

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
    # board = chess.Board()
    # board = chess.Board('8/8/8/8/8/8/4k3/RR5K w Q - 0 1')
    board = chess.Board('8/8/8/4K3/rr5k/8/8/8 w - - 0 1')
    board_states = []
    outcome = playGame(board, chess.WHITE, board_states)
    printOutcome(outcome)

if __name__ == "__main__":
    main()