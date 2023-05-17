# TeekoPlayer
Play Teeko against an AI player

# How to Play
Teeko is a 2 player game played on a 5 by 5 board. Each player is randomly assigned either red or black. Each player has 4 tokens of their color. The goal is to get either 4 pieces in a row in any direction (vertical, horizontal, or diagonol) or 4 in 2x2 box. 
With the black player starting, each player takes turns placing a token until all have been placed. If no player has won, then players take turns moving their pieces by 1 space until a player wins. 

# AI Player
The AI player uses a MiniMax algorithm to choose its moves. It assumes that each person will play optimally and checks some of the possible future positions for the best one. To avoid being time and computing intensive, it uses a heuristic to check which near-future states are best instead of searching through all future states for the best move. 

# Running the Game
Upon running the program, a "board" with rows labeled 0-4 and columns labeled A-E will be displayed. Either the user or the AI will be randomly chosen as black, and will get to play first. To play, the user must type in the coordinates of the square they want to drop their token. After all 4 tokens are dropped, the user must specify which token they want to pick up and move to an adjacent location.  
The game continues until either the user or AI wins.
