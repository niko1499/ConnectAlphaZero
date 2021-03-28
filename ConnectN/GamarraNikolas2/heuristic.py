###########################
# Heuristic data tree     #
###########################
from __future__ import annotations

from typing import Tuple, Optional

from board import Board
import math

debug_level = 0


class Heuristic:
    def __init__(self, data: Tuple[Board, int], root_player: int, parent_score: int = 0):
        self.board = data[0]  # holds 2d array of board
        self.col = data[1]  # holds column where last move was made
        self.children = []  # holds object of this class in tree data structure
        self.root_player = root_player  # keeps record of root player so heuristic can be informed by it
        self.score = parent_score + self.calc_move_score(self.board, self.col)  # calculates heuristic for node

    def add_child(self, obj: Heuristic):
        """adds a child to tree"""
        self.children.append(obj)

    @property
    def last_player(self):
        # Return the player who made the move to reach this heuristic node
        if self.board.player == 1:
            return 2
        else:
            return 1

    def calc_move_score(self, board: Board, col: int) -> int:
        """calculates heuristic"""
        score = 0
        x = col
        y = self.get_depth(
            col) or 0  # The or 0 is to guarantee, in case of no tiles in the column (unlikely) that it still works

        if self.wining_move(x, y):
            score += 9001  # OVER 9000!

        if (debug_level >= 2):
            if self.board.player == 2:
                print("\033[1;32;40m  --START CALC SCORE--")
                pass
            else:
                print("\033[1;34;40m  --START CALC SCORE--")
                pass
        # find center of board
        center = board.w / 2
        center = int(center)

        # Reward proximity to center
        score -= int(abs(self.col - center))  # -= works for some weird reason

        # reward dense friendly areas any direction proportional to length
        score += math.pow(2,self.sum_lines(x, y))
        score += self.density(x, y, 1)*.8 # applied multiple times so multiplier is small
        score += self.density(x, y, 2)*.5
        score += self.density(x, y, 3)*.3

        # reward gap placement
        score += self.gap_score(x, y) * 1.65 # over 2 gives losses

        # give super high priority to blocking moves that prevent loss
        if self.block_nless1(x, y) >= self.board.n - 1:
            score += 99999

        # give slight advantage to blocking moves of small sizes
        score += self.block_nless1(x, y) * 2

        # set opponent score negative and BE AGGRESSIVE by some factor(breaks ties between win loss alpha beta)
        if self.last_player != self.root_player:
            score = score * -.9
        else:
            score = score * 1.01

        if debug_level >= 2:# put conditional debug here
            print("Player Placing", self.last_player)
            self.board.print_it()
            print("score: {}, col: {}".format(score, self.col))

            print(" --END CALC SCORE--")

        return score

    def get_depth(self, x) -> Optional[int]:
        """gets y val of dropped piec in col x. Returns None if no pieces"""
        y = 0

        # Search for first gap
        while self.is_bounded(x, y) and self.board.board[y][x] != 0:
            y += 1

        if y == 0:
            # No tiles found
            return None
        else:
            # Return index below first gap found
            return y - 1

    def block_nless1(self, x, y):
        char = self.get_cell(x, y)

        if char == 2:
            opponent = 1
        else:
            opponent = 2
        length = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if debug_level>3:
                    print("ij",i,",",j)
                dx = i - x
                dy = j - y
                if (self.is_bounded(i, j)):
                    if (self.get_cell(i, j) == opponent):
                        length=max(length, self.walk_line_full(i, j, dx, dy))
                        if debug_level>3:
                            print("-----------HERE",i,",",j,",",dx,",",dy)

        # special condition for n-2 ungurarded
        if length == self.board.n - 2:
            if (self.get_cell(i + (dx * (length + 1)), j + (dy + (length + 13))) == 0):
                length = self.board.n
                if debug_level>3:
                    print("special cond")
        if debug_level>3:
            print("lenghtblocker",length)
        return length

    def sum_lines(self, x, y):
        """return the sum of all connected lines"""
        total = 0
        total += total + self.walk_line(x, y, 1, 1)
        total += self.walk_line(x, y, 0, 1)
        total += self.walk_line(x, y, -1, 1)
        total += self.walk_line(x, y, 1, 0)
        total += self.walk_line(x, y, -1, 0)
        total += self.walk_line(x, y, 1, -1)
        total += self.walk_line(x, y, 0, -1)
        total += self.walk_line(x, y, -1, -1)
        return total

    def walk_line_full(self, x, y, dx, dy):
        total = 0  # Count the first symbol always
        total += total + self.walk_line(x, y, dx, dy)
        total += self.walk_line(x, y, -dx, -dy)
        return total + 1

    def density(self, x, y, size):
        points = 0
        if (self.is_bounded(x, y)):
            for i in range(x - size, x + size):
                for j in range(y - size, y + size):
                    if self.is_bounded(i, j):
                        if self.get_cell(i, j) == self.get_cell(x, y):
                            points += 1
        return points

    def wining_move(self, x, y):
        if (self.walk_line_full(x, y, 1, 1) >= self.board.n or self.walk_line_full(x, y, 1,
                                                                                   0) >= self.board.n or self.walk_line_full(
            x, y, 1, -1) >= self.board.n or self.walk_line_full(x,y,0,1)>=self.board.n):
            return True
        else:
            return False

    def gap_score(self, x, y):
        # check left
        score = 1
        i = x - 1
        j = y
        if self.is_bounded(i - 1, j):
            if (self.get_cell(i, j) == 0):
                if (self.get_cell(i - 1, j) == self.get_cell(x, y)):  # if the cell to the side is empty
                    if self.get_cell(i - 1, j) == self.get_cell(x, y):
                        score += self.walk_line_full(i - 1, j, -1, 0)
                        score += self.walk_line_full(x, y, 1, 0)
            if (self.get_cell(i, j + 1) == 0):
                if (self.get_cell(i - 1, j + 2) == self.get_cell(x, y)):  # if the cell to the side is empty
                    if self.get_cell(i - 1, j + 2) == self.get_cell(x, y):
                        score += self.walk_line_full(i - 1, j + 2, -1, 1)
                        score += self.walk_line_full(x, y, 1, -1)

            if (self.get_cell(i, j - 1) == 0):
                if (self.get_cell(i - 1, j - 2) == self.get_cell(x, y)):  # if the cell to the side is empty
                    if self.get_cell(i - 1, j - 2) == self.get_cell(x, y):
                        score += self.walk_line_full(i - 1, j - 2, -1, -1)
                        score += self.walk_line_full(x, y, 1, 1)

        # check right
        i = x + 1
        if self.is_bounded(i + 1, j):
            if (self.get_cell(i, j) == 0):
                if (self.get_cell(i + 1, j) == self.get_cell(x, y)):  # if the cell to the side is empty
                    if self.get_cell(i + 1, j) == self.get_cell(x, y):
                        score += self.walk_line_full(i + 1, j, +1, 0)
                        score += self.walk_line_full(x, y, -1, 1)
            if (self.get_cell(i, j + 1) == 0):
                if (self.get_cell(i + 1, j + 2) == self.get_cell(x, y)):  # if the cell to the side is empty
                    if self.get_cell(i + 1, j + 2) == self.get_cell(x, y):
                        score += self.walk_line_full(i - 1, j + 2, 1, 1)
                        score += self.walk_line_full(x, y, -1, -1)
            if (self.get_cell(i, j - 1) == 0):
                if (self.get_cell(i + 1, j - 2) == self.get_cell(x, y)):  # if the cell to the side is empty
                    if self.get_cell(i + 1, j - 2) == self.get_cell(x, y):
                        score += self.walk_line_full(i - 1, j - 2, 1, -1)
                        score += self.walk_line_full(x, y, -1, 1)
        return score

    def walk_line(self, x, y, dx, dy) -> int:
        """Return line length of identical tokens exists starting at (x,y)
           in direction (dx,dy)"""
        length = 0

        # Get the starting char
        char = self.board.board[y][x]

        # Take the first step
        x += dx
        y += dy

        # Loop until out of bound or we break
        while self.is_bounded(x, y):
            if self.board.board[y][x] == char:
                length += 1
            else:
                break
            x += dx
            y += dy

        # Since we technically double count the first character, skip it.
        return length

    def is_bounded(self, x, y):
        return x >= 0 and x < self.board.w and y >= 0 and y < self.board.h

    def get_cell(self, x, y) -> Optional[int]:
        if self.is_bounded(x, y):
            return self.board.board[y][x]

    def has_children(self):  # helper function to check if at bottom of tree
        if len(self.children) > 0:
            return True
        else:
            return False
