import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.has_not_moved = True

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        self.player = brd.player
        if(self.player == 2):
            self.opp = 1
        else:
            self.opp = 2
        if self.player == 1 and self.has_not_moved is True:
            return math.floor(brd.w/2)
        self.has_not_moved = False
        best_value = self.minimax(brd, 3, 1, True, -math.inf, math.inf)
        col_is = self.col
        for successor, col in self.get_successors(brd):
            if col == self.col:
                value = self.check_lines(successor)
                if value < -5000:
                    self.minimax(brd, 3, self.max_depth-2, True, -math.inf, math.inf)

        return self.col


    def board_line_values(self, brd, x, y, dx, dy):
        """Return True if a line of identical tokens exists starting at (x,y)
           in direction (dx,dy)"""

        #before checking against these points try against brd.n

        blocked_one_side_edge = False
        disjoint = False
        player1_value = 0
        player2_value = 0
        player1_streak = 0
        player2_streak = 0

        #checks a cell to see if there is a piece there
        for i in range(max(brd.h, brd.w)):
                x_index = x + (dx * (i+1))
                y_index = y + (dy * (i+1))

                if (-1 < x_index < brd.h) and (-1 < y_index < brd.w):
                    if brd.board[x_index][y_index] != 0:

                        if ((x_index == 0 or x_index == brd.h) and dx != 0) or ((y_index == 0 or y_index == brd.w) and dy != 0):
                            blocked_one_side_edge = True

                        if brd.board[x_index][y_index] == 1:

                            if player2_streak:
                                if not blocked_one_side_edge or disjoint:
                                    disjoint = False
                                    if player2_streak == brd.n - 1:
                                        player2_value += 10000
                                    player2_value += player2_streak * 1.5 * 100
                                    player2_streak = 0
                                    blocked_one_side_edge = True
                            else:
                                player1_streak += 1

                            player1_streak += 1

                        if brd.board[x_index][y_index] == 2:

                            if player1_streak:
                                if not blocked_one_side_edge or disjoint:
                                    disjoint = False
                                    if player1_streak == brd.n - 1:
                                        player1_value += 10000
                                    player1_value += player1_streak * 1.5 * 100
                                    player1_streak = 0
                                    blocked_one_side_edge = True
                            else:
                                player2_streak += 1

                            player2_streak += 1


                    if (player1_streak or player2_streak) and ((x_index == brd.h and dx != 0) or (y_index == brd.w and dy != 0)) and disjoint:

                        if player2_streak:
                            if player2_streak == brd.n - 1:
                                player2_value += 15000
                            player2_value += player2_streak * 5 * 100
                            player2_streak = 0

                        if player1_streak:
                            if player1_streak == brd.n - 1:
                                player1_value += 15000
                            player1_value += player1_streak * 5 * 100
                            player1_streak = 0

                    elif (player1_streak or player2_streak) and ((x_index == brd.h and dx != 0) or (y_index == brd.w and dy != 0)):

                        if player2_streak and not blocked_one_side_edge:
                            if player2_streak == brd.n - 1:
                                player2_value += 15000
                            player2_value += player2_streak * 1.5 * 100
                            player2_streak = 0

                        elif player1_streak and not blocked_one_side_edge:
                            if player1_streak == brd.n - 1:
                                player1_value += 15000
                            player1_value += player1_streak * 1.5 * 100
                            player1_streak = 0

                    elif (player2_streak or player1_streak) and not blocked_one_side_edge:
                        if player1_streak:
                            player1_value += player1_streak * 10 * 100
                            if player1_streak == brd.n - 2:
                                player1_value += 10000

                        else:
                            player2_value += player2_streak * 10 * 100
                            if player2_streak == brd.n - 2:
                                player2_value += 10000

                    elif player2_streak or player1_streak:
                        disjoint = True

                    else:
                        blocked_one_side_edge = False

        if self.player == 1:
            if player2_value > 10000:
                return -9999999
            if player1_value > 10000:
                return 9999999
            return player1_value - player2_value
        else:
            if player1_value > 10000:
                return -9999999
            if player2_value > 10000:
                return 9999999
            return player2_value - player1_value


    def check_lines(self, brd):
        """Return True if a line of identical symbols exists starting at (x,y)
           in any direction"""
        value = 0
        for row in range(0, brd.h):
            value += self.board_line_values(brd, row, 0, 1, 0)  # Horizontal
        for column in range(0, brd.w):
            value += self.board_line_values(brd, 0, column, 0, 1)  # Vertical

        for r in range(0, brd.h):
            for c in range(0, brd.w):
                if r == 0 or c == 0:
                    value += self.board_line_values(brd, r, c, 1, 1)  # Diagonal up

        for r in range(brd.h - 1, -1, -1):
            for c in range(brd.w - 1, -1, -1):
                if r == brd.w or c == brd.h:
                    value += self.board_line_values(brd, r, c, 1, -1) # Diagonal down

        return value


    def evaluation(self, brd):
        return self.check_lines(brd)


    def minimax(self, brd, column, depth, isMaximizingPlayer, alpha, beta):
        if self.max_depth == depth:
            return self.evaluation(brd)

        if isMaximizingPlayer:
            best_value = -math.inf
            for successor, col in self.get_successors(brd):
                value = self.minimax(successor, col, depth+1, False, alpha, beta)
                best_value = max(best_value, value)
                if best_value == value:
                    self.col = col
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value

        else:
            best_value = math.inf
            for successor, col in self.get_successors(brd):
                value = self.minimax(successor, col, depth+1, True, alpha, beta)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value


    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ

THE_AGENT = AlphaBetaAgent("GumiennyKamil", 4)