# ChipotleBot

A chessbot that will hopefully beat a friend of mine and win me two Chipotle meals. For now, a scrappy game simulator against a decent opponent in the terminal lol. Made using the [python chess library](https://python-chess.readthedocs.io/en/latest/) and inspired HEAVILY by [Sebastian Lague's amazing videos on chessbots](https://www.youtube.com/playlist?list=PLFt_AvWsXl0cvHyu32ajwh2qU1i6hl77c).

## So Far
- Implemented minimax search algorithm with alpah-beta pruning
- Considered piece positioning in evaluation with piece-square tables (copied from [Chess Programming Wiki](https://www.chessprogramming.org/Simplified_Evaluation_Function))

## To Do
- Quiescent search
- Lookup table for positions already searched
- Making the most of alpha-beta pruning by ordering moves before searching them
- More intricate piece-square tables (king start vs. endgame)
