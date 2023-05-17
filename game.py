import random
import copy
import time

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). 

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. 
        """

        drop_phase = self.checkDropPhase(state) 
        
        move = []
        
        val, bestState = self.max_value(state, 0)
        newRow, newCol = self.findNewPiecePlace(state, bestState)

        move.append((newRow, newCol))

        if drop_phase:
            return move
        else:
            
            origRow, origCol = self.findOldPiecePlace(state, bestState)

            move.append((origRow, origCol))

        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1

        # check / diagonal wins
        for row in range(2):
            for col in [3,4]:
                if state[row][col] != ' ' and state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
                    return 1 if state[row][col]==self.my_piece else -1
                
        # check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row][col+1] == state[row+1][col] == state[row+1][col+1]:
                    return 1 if state[i][col]==self.my_piece else -1
                
        return 0 # no winner yet


    def heuristic_game_value(self, state):
        if self.game_value != 0:
            return self.game_value(state)
        
        myMostLikelyScoringRoute = 0
        oppMostLikelyScoringRoute = 0

        myScore = 0
        oppScore = 0

        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                    myScore = myScore + 1
                elif state[i][j] == self.opp:
                    oppScore = oppScore + 1
            if myScore > myMostLikelyScoringRoute:
                myMostLikelyScoringRoute = myScore
            if oppScore > oppMostLikelyScoringRoute:
                oppMostLikelyScoringRoute = oppScore
        myScore = 0
        oppScore = 0

        for i in range(5):
            for j in range(5):
                if state[j][i] == self.my_piece:
                    myScore = myScore + 1
                elif state[j][i] == self.opp:
                    oppScore = oppScore + 1
            if myScore > myMostLikelyScoringRoute:
                myMostLikelyScoringRoute = myScore
            if oppScore > oppMostLikelyScoringRoute:
                oppMostLikelyScoringRoute = oppScore
        myScore = 0
        oppScore = 0

        for i in range(2):
            for j in range(2):
                for x in range(4):
                    if state[i+x][j+x] == self.my_piece:
                        myScore = myScore + 1
                    elif state[i+x][j+x] == self.opp:
                        oppScore = oppScore + 1
            if myScore > myMostLikelyScoringRoute:
                myMostLikelyScoringRoute = myScore
            if oppScore > oppMostLikelyScoringRoute:
                oppMostLikelyScoringRoute = oppScore
        myScore = 0
        oppScore = 0

        for i in range(2):
            for j in [3,4]:
                for x in range(4):
                    if state[i+x][j-x] == self.my_piece:
                        myScore = myScore + 1
                    elif state[i+x][j-x] == self.opp:
                        oppScore = oppScore + 1
            if myScore > myMostLikelyScoringRoute:
                myMostLikelyScoringRoute = myScore
            if oppScore > oppMostLikelyScoringRoute:
                oppMostLikelyScoringRoute = oppScore
        myScore = 0
        oppScore = 0

        for i in range(4):
            for j in range(4):
                for x in range(2):
                    if state[i][j+x] == self.my_piece:
                        myScore = myScore + 1
                    if state[i+1][j+x] == self.my_piece:
                        myScore = myScore + 1
                    elif state[i][j+x] == self.opp:
                        oppScore = oppScore + 1
                    elif state[i+1][j+x] == self.opp:
                        oppScore = oppScore + 1
            if myScore > myMostLikelyScoringRoute:
                myMostLikelyScoringRoute = myScore
            if oppScore > oppMostLikelyScoringRoute:
                oppMostLikelyScoringRoute = oppScore


        if myMostLikelyScoringRoute>oppMostLikelyScoringRoute:
            return myMostLikelyScoringRoute/4
        elif myMostLikelyScoringRoute<oppMostLikelyScoringRoute:
            return (-1*oppMostLikelyScoringRoute)/4
        else:
            return 0

    #Gets succesor states
    def succ(self, state, turn):
        succList = []
        r, b = self.getPieceLocations(state)
        
        if turn == 'r':
            mark = r
        else:
            mark = b

        if self.checkDropPhase(state):
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == ' ':
                        copyState = copy.deepcopy(state)
                        copyState[i][j] = turn
                        succList.append(copyState)
        else:
            for i in range(4):
                #up
                if mark[i][0]>0 and state[mark[i][0]-1][mark[i][1]] == ' ':
                    copyState = copy.deepcopy(state)
                    copyState[mark[i][0]-1][mark[i][1]] = copyState[mark[i][0]][mark[i][1]]
                    copyState[mark[i][0]][mark[i][1]] = ' '
                    succList.append(copyState)
                #down
                if mark[i][0]<4 and state[mark[i][0]+1][mark[i][1]] == ' ':
                    copyState = copy.deepcopy(state)
                    copyState[mark[i][0]+1][mark[i][1]] = copyState[mark[i][0]][mark[i][1]]
                    copyState[mark[i][0]][mark[i][1]] = ' '
                    succList.append(copyState)
                #right
                if mark[i][1]<4 and state[mark[i][0]][mark[i][1]+1] == ' ':
                    copyState = copy.deepcopy(state)
                    copyState[mark[i][0]][mark[i][1]+1] = copyState[mark[i][0]][mark[i][1]]
                    copyState[mark[i][0]][mark[i][1]] = ' '
                    succList.append(copyState)
                #left
                if mark[i][1]>0 and state[mark[i][0]][mark[i][1]-1] == ' ':
                    copyState = copy.deepcopy(state)
                    copyState[mark[i][0]][mark[i][1]-1] = copyState[mark[i][0]][mark[i][1]]
                    copyState[mark[i][0]][mark[i][1]] = ' '
                    succList.append(copyState)
                #up left
                if mark[i][0]>0 and mark[i][1]>0 and state[mark[i][0]-1][mark[i][1]-1] == ' ':
                    copyState = copy.deepcopy(state)
                    copyState[mark[i][0]-1][mark[i][1]-1] = copyState[mark[i][0]][mark[i][1]]
                    copyState[mark[i][0]][mark[i][1]] = ' '
                    succList.append(copyState)
                #up right
                if mark[i][0]>0 and mark[i][1]<4 and state[mark[i][0]-1][mark[i][1]+1] == ' ':
                    copyState = copy.deepcopy(state)
                    copyState[mark[i][0]-1][mark[i][1]+1] = copyState[mark[i][0]][mark[i][1]]
                    copyState[mark[i][0]][mark[i][1]] = ' '
                    succList.append(copyState)
                #down right
                if mark[i][0]<4 and mark[i][1]<4 and state[mark[i][0]+1][mark[i][1]+1] == ' ':
                    copyState = copy.deepcopy(state)
                    copyState[mark[i][0]+1][mark[i][1]+1] = copyState[mark[i][0]][mark[i][1]]
                    copyState[mark[i][0]][mark[i][1]] = ' '
                    succList.append(copyState)
                #down left
                if mark[i][0]<4 and mark[i][1]>0 and state[mark[i][0]+1][mark[i][1]-1] == ' ':
                    copyState = copy.deepcopy(state)
                    copyState[mark[i][0]+1][mark[i][1]-1] = copyState[mark[i][0]][mark[i][1]]
                    copyState[mark[i][0]][mark[i][1]] = ' '
                    succList.append(copyState)

        return succList

    #minimax alg
    def max_value(self, state, depth):
        bestState = state
        if self.game_value(state) == 1 or  self.game_value(state) == -1:
            return self.game_value(state), state
        if depth >= 3:
            return self.heuristic_game_value(state), state
        else:
            a = float('-inf')
            for s in self.succ(state, self.my_piece):
                output = self.min_value(s, depth+1)
                a = max(a, output[0])
                if a == output[0]:
                    bestState = s
            return a, bestState

    def min_value(self, state, depth):
        bestState = state
        if self.game_value(state) == 1 or  self.game_value(state) == -1:
            return self.game_value(state), state
        if depth >= 3:
            return self.heuristic_game_value(state), state
        else:
            B = float('inf')
            for s in self.succ(state, self.opp):
                output = self.max_value(s, depth+1)
                B = min(B, output[0])
                if B == output[0]:
                    bestState = s
            return B, bestState

    #Get Piece Locations, with my_piece coming first
    def getPieceLocations(self, state):
        rLocations = []
        bLocations = []

        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 'r':
                    rLocations.append([i,j])
                elif state[i][j] == 'b':
                    bLocations.append([i,j])

        return rLocations, bLocations


    #find if its a drop phase
    def checkDropPhase(self, state):
        markerCount = 0
        
        for i in state:
            for j in i:
                if j != ' ':
                    markerCount = markerCount+1
        
        if markerCount==8:
            return False
        elif markerCount>8:
            print("Error: There are more than 8 markers on the board?")
            return None
        else:
            return True
    
    def findNewPiecePlace(self, origState, newState):
        for row in range(5):
            for col in range(5):
                if origState[row][col] != newState[row][col] and origState[row][col] == ' ':
                    return row, col
                
    def findOldPiecePlace(self, origState, newState):
        for row in range(5):
            for col in range(5):
                if origState[row][col] != newState[row][col] and origState[row][col] != ' ':
                    return row, col
        

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():

    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
