# TeekoPlayer
Play Teeko against an AI player

# How to Play
![image](https://github.com/arnavnair220/TeekoPlayer/assets/67218442/5572fc62-67ba-44b4-a03d-d15837973d22)

Teeko is a 2 player game played on a 5 by 5 board. Each player is randomly assigned either red or black. Each player has 4 tokens of their color. The goal is to get either 4 pieces in a row in any direction (vertical, horizontal, or diagonol) or 4 in 2x2 box. 
With the black player starting, each player takes turns placing a token until all have been placed. If no player has won, then players take turns moving their pieces by 1 space until a player wins. 

# AI Player
The AI player uses a MiniMax algorithm to choose its moves. It assumes that each person will play optimally and checks some of the possible future positions for the best one. To avoid being time and computing intensive, it uses a heuristic to check which near-future states are best instead of searching through all future states for the best move. 

# Running the Game
Upon running the program, a "board" with rows labeled 0-4 and columns labeled A-E will be displayed. Either the user or the AI will be randomly chosen as black, and will get to play first. To play, the user must type in the coordinates of the square they want to drop their token. After all 4 tokens are dropped, the user must specify which token they want to pick up and move to an adjacent location.  
The game continues until either the user or AI wins.

Sample Gameplay:
```
Hello, this is Samaritan
0:
1:
2:
3:
4:
   A B C D E
b's turn
Move (e.g. B3): E4
0:
1:
2:
3:
4:         b
   A B C D E
r moved at D4
0:
1:
2:
3:
4:       r b
   A B C D E
b's turn
Move (e.g. B3): E3
0:
1:
2:
3:         b
4:       r b
   A B C D E
r moved at C4
0:
1:
2:
3:         b
4:     r r b
   A B C D E
b's turn
Move (e.g. B3): E2
0:
1:
2:         b
3:         b
4:     r r b
   A B C D E
r moved at E1
0:
1:         r
2:         b
3:         b
4:     r r b
   A B C D E
b's turn
Move (e.g. B3): B3
0:
1:         r
2:         b
3:   b     b
4:     r r b
   A B C D E
r moved at B4
0:
1:         r
2:         b
3:   b     b
4:   r r r b
   A B C D E
b's turn
Move from (e.g. B3): E2
Move to (e.g. B3): D2
0:
1:         r
2:       b
3:   b     b
4:   r r r b
   A B C D E
r moved from D4
  to C3
0:
1:         r
2:       b
3:   b r   b
4:   r r   b
   A B C D E
b's turn
Move from (e.g. B3): E4
Move to (e.g. B3): D3
0:
1:         r
2:       b
3:   b r b b
4:   r r
   A B C D E
r moved from C4
  to D4
0:
1:         r
2:       b
3:   b r b b
4:   r   r
   A B C D E
b's turn
Move from (e.g. B3): D2
Move to (e.g. B3): E2
0:
1:         r
2:         b
3:   b r b b
4:   r   r
   A B C D E
r moved from D4
  to C4
0:
1:         r
2:         b
3:   b r b b
4:   r r
   A B C D E
b's turn
Move from (e.g. B3): B3
Move to (e.g. B3): C2
0:
1:         r
2:     b   b
3:     r b b
4:   r r
   A B C D E
r moved from C3
  to D2
0:
1:         r
2:     b r b
3:       b b
4:   r r
   A B C D E
b's turn
Move from (e.g. B3): E3
Move to (e.g. B3): E4
0:
1:         r
2:     b r b
3:       b
4:   r r   b
   A B C D E
r moved from C4
  to C3
0:
1:         r
2:     b r b
3:     r b
4:   r     b
   A B C D E
AI wins! Game over.
```
