# General
- [x] learn an actual python testing library and make real tests lol
- [x] make this the backend for a react page where you can drag and drop the pieces

# Frontend
- [x] add (naive) point evaluator to board
- [ ] add ability to click to move
- [ ] add ability to premove

# MoveMaker
- [x] Write tests, make sure minimax algorithm is,, actually working
- [x] Implement alpha-beta pruning on make_move
- [x] import a TON of pro games and have the bot follow them as long as possible (or just manny well-established openings)

- [ ] When it finds a forced mate, play those moves instead of just knowing you have it lol dummy
- [x] Implement quiescent search
- [ ] improve endgame (move towards other king, for example)

# Evaluator
- [x] change depth as number of pieces on the board decreases
- [x] implement pawn evaluation to help early game
- [x] implement piece tables to help all game
- [ ] Lookup table for already evaluated positions (will need to instantiate Evaluator loll)
- [ ] guess move ordering before searching them to get the most out of alpha-beta pruning
