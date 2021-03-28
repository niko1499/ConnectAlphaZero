import math
import agent
import board

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
        # number of points for a winning board
        self.WIN = 1234560

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        freecols = brd.free_cols()

        alpha, move = self.evalBoard(brd, -100000, 100000, self.max_depth, self.player, True)
        #print(move)
        # come up with a better solution TODO
#        if move not in freecols:
#            move = freecols[0]

        return move

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

    # evaluates a board using the negamax version of the minimax algorithm
    #
    # PARAM [board.Board] brd: the board state to evaluate
    # PARAM [int] alpha: the minimum score
    # PARAM [int] beta: the maximum score
    # PARAM [int] depth: the depth down the board to evaluate
    # PARAM [int] player: the player whose moves are being evaluated
    # PARAM [bool] firstCall (optional): if this is the first call
    # RETURN [int, int]: the alpha value of the board, the maximizing move to make
    def evalBoard(self, brd, alpha, beta, depth, player, firstCall = False):
        """Evaluates what move to make based on the current board, using the Negamax algorithm"""
        # if this board is a winning board, return a large number so that we will choose it
        for y in range(brd.h):
            for x in range(brd.w):
                if self.is_any_line_at(x,y, brd, player):
                    return self.WIN, -1

        # if we've reached max depth, just return the score
        # the higher levels will deal with all the pruning and minimaxing logic
        if player == 1:
            opponent = 2
        else:
            opponent = 1
        if depth == 0:
            score = (self.scoreBoard(brd, player) - self.scoreBoard(brd, opponent))
            return score, -1

        if alpha >= beta:
            return beta, -1

        succs = self.get_successors(brd)
        bestMove = -1
        for succ, move in succs:
            if bestMove == -1:
                bestMove = move

            if firstCall:
                score, next_move = self.evalBoard(succ, alpha, beta, depth - 1, player)
            else:
                score, next_move = self.evalBoard(succ, -1 * beta, -1 * alpha, depth - 1, opponent)
                score = -1 * score
            
            if score >= beta:
                return score, move
            if score > alpha:
                alpha = score
                bestMove = move
        return alpha, bestMove

    # gives a board a score according to my heuristics
    # PARAM [board.Board] brd: the board being scored
    # PARAM [int] player: the player to look for a line for
    # RETURN [int]: the board's score
    def scoreBoard(self, brd, player):
        """calculates a score for a how good a board is using my heuristics"""
        # sum of vertical points
        vertiPoints = 0
        # sum of horizontal points
        horizPoints = 0
        # sum of diagonal points going up/right
        diagUPoints = 0
        # sum of diagonal points going down/right
        diagDPoints = 0
        # total points
        totalPoints = 0

        # calculate sum of vertical points
        for x in range(brd.w):
            points = self.scoreLine(x, 0, 0, 1, brd, player)
            vertiPoints += points
            if vertiPoints >= self.WIN:
                return self.WIN
        if vertiPoints < 0:
            vertiPoints = 0
        totalPoints = vertiPoints

        # calculate sum of horizontal points
        for y in range(brd.h):
            points = self.scoreLine(0, y, 1, 0, brd, player)
            horizPoints += points
            if (horizPoints >= self.WIN):
                return self.WIN
        if horizPoints < 0:
            horizPoints = 0
        totalPoints = totalPoints + horizPoints

        # calculate sum of diagonal up
        for y in range(brd.h):
            points = self.scoreLine(0, y, 1, -1, brd, player)
            diagUPoints += points
            if (diagUPoints >= self.WIN):
                return self.WIN
        for x in range(1, brd.w):
            points = self.scoreLine(x, brd.h - 1, 1, -1, brd, player)
            diagUPoints += points
            if (diagUPoints >= self.WIN):
                return self.WIN
        if diagUPoints < 0:
            diagUPoints = 0
        totalPoints = totalPoints + diagUPoints

        # calculate sum of diagonal down
        for y in range(brd.h):
            points = self.scoreLine(0, y, 1, 1, brd, player)
            diagDPoints += points
            if (diagDPoints >= self.WIN):
                return self.WIN
        for x in range(brd.w):
            points = self.scoreLine(x, 0, 1, 1, brd, player)
            diagDPoints += points
            if (diagDPoints >= self.WIN):
                return self.WIN
        if diagDPoints < 0:
            diagDPoints = 0
        totalPoints = totalPoints + diagDPoints

        return totalPoints

    # gives a score for a line according to my heuristics
    # PARAM [int] x: the x coordinate to start the line in
    # PARAM [int] y: the y coordinate to start the line in
    # PARAM [int] dx: the direction to mo in horizontally
    # PARAM [int] dy: the direction to move in verrtically
    # PARAM [board.Board] brd: the board to score from
    # PARAM [int] player: the player to look for a line for
    # RETURN [int]: the score for that line
    def scoreLine(self, x, y, dx, dy, brd, player):
        """Calculates a score for a single line on a board using my heuristics"""
        if player == 1:
            opponent = 2
        else:
            opponent = 1
        # number of points in the line so far
        points = 0

        # True if the last point that was checked was empty or own piece
        # False if the last point that was checked was out of bounds or an opponent piece
        lastPointClear = False

        # True if the last point that wasn't own piece was empty
        # False if the last point that wasn't own piece was opponents
        lineStartClear = False

        # number of consecutive pieces that were mine currently
        numConsecutive = 0
        numConsecutiveOpp = 0

        while (x < brd.w and y < brd.h and x >= 0 and y >= 0):
            # if piece belongs to me
            if brd.board[y][x] == player:
                # give me one point for owning the piece
                points += 1
                # if the last point checked was empty, I can expand in that direction, so give me a point
                if lastPointClear and lineStartClear:
                    points += 1
                # give me an extra point for having consecutive pieces
                if numConsecutive > 0:
                    points += 1
                # increase the number of consecutive points belonging to me
                numConsecutive += 1
                # if I have N in a row, its a winning board, so set the points to an ungodly number
                # to incentivize picking this board
                if numConsecutive >= brd.n:
                    return self.WIN
                # this point is not empty, but call it that so the math works out
                lastPointClear = True
                # give some bonus for blocking an opponent
                if numConsecutiveOpp > 1:
                    points += 2
                # set the number of consecutive opponent piece to 0 since this is mine
                numConsecutiveOpp = 0

            elif brd.board[y][x] == opponent:
                # if this piece blocks less than N of my own pieces in between opponents pieces and/or wall,
                # those pieces cannot be part of N in a row in this direction, so they shoouldn't give me
                # any points
                if not lineStartClear:
                    points -= ((2 * numConsecutive) - 1)
                # if this piece is next to one of my pieces that isn't blocked on the other side, it loses
                # its 1 point bonus for not being blocked in any direction
                elif numConsecutive > 0:
                    points -= 1
                # if last piece was mine it blocks this opponent piece, so give me a bonus
                if numConsecutive > 0:
                    # i know this cancels out the last line, but it needs to give me points
                    # even if I lose all the points from being canceled out
                    points += 2
                # the last point is now not empty
                lastPointClear = False
                # if the next point belongs to me, any consecutive pieces from is were blocked at the start
                lineStartClear = False
                # there are now 0 consecutive pieces belonging to me
                numConsecutive = 0
                # increase the number of consecutive pieces belonging to opponent
                numConsecutiveOpp += 1
                # if opponent has N in a row, they win. BAD. return an ungodly low number to prevent this from
                # being picked
                if numConsecutiveOpp >= brd.n:
                    return -1 * self.WIN

            # if there is no piece here
            elif brd.board[y][x] == 0:
                # the last point checked (this one) is clear
                lastPointClear = True
                # if a series of consecutive pieces belonging to me starts, it is unblocked on this side
                lineStartClear = True
                # there are now 0 consecutive pieces belonging to me or my opponent at this point
                numConsecutive = 0
                numConsecutiveOpp = 0

            x += dx
            y += dy

        # if there is an own piece on the end wall, it might have gotten an extra
        # point for being clear on both sides, but its not actually so take it away
        if numConsecutive > 0 and lineStartClear:
            points -= 1

        # if there is a set of consecutive own pieces against the end wall and
        # there is an opponent piece immediately before them, all their points are useless
        # (at least in this direction) so take them away
        elif numConsecutive > 0 and not lineStartClear:
            points -= ((2 * numConsecutive) - 1)

        return points


# copied and slightly modified from board.py since that one didn't work the way I needed it to
    # Check if a line of identical tokens exists starting at (x,y) in direction (dx,dy)
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # PARAM [int] dx: the step in the x direction
    # PARAM [int] dy: the step in the y direction
    # PARAM [board.Board] brd: the board
    # PARAM [int] player: the player to look for a line for
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise
    def is_line_at(self, x, y, dx, dy, brd, player):
        """Return True if a line of identical tokens exists starting at (x,y) in direction (dx,dy) that belongs to player"""
        # Avoid out-of-bounds errors
        if ((x + (brd.n-1) * dx >= brd.w) or
            (y + (brd.n-1) * dy < 0) or (y + (brd.n-1) * dy >= brd.h)):
            return False
        # Get token at (x,y)
        t = brd.board[y][x]

        if t == 0 or t != player:
            return False
        # Go through elements
        for i in range(1, brd.n):
            if brd.board[y + i*dy][x + i*dx] != t:
                return False
        return True

    # Check if a line of identical tokens exists starting at (x,y) in any direction
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # PARAM [board.Board] brd: the board
    # PARAM [int] player: the player to look for a line for
    # RETURN [Bool]: True if n tokens of the same type have been found, False otherwise
    def is_any_line_at(self, x, y, brd, player):
        """Return True if a line of identical tokens exists starting at (x,y) in any direction that belongs to playerr"""
        return (self.is_line_at(x, y, 1, 0, brd, player) or # Horizontal
                self.is_line_at(x, y, 0, 1, brd, player) or # Vertical
                self.is_line_at(x, y, 1, 1, brd, player) or # Diagonal up
                self.is_line_at(x, y, 1, -1, brd, player)) # Diagonal down


THE_AGENT = AlphaBetaAgent("LessardPhilippe", 4)