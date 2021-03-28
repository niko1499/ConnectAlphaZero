import math
from typing import List, Tuple

from agent import Agent
from board import Board
from . import heuristic


# from . import Heuristic

debug_level=0
threshold=9000


###########################
# Alpha-Beta Search Agent #
###########################
class AlphaBetaAgent(Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):  # main routine invoked by game simulator
        """Search for the best move (choice of column for the token)"""
        # Your code here

        # create heuristic at specified depth for the current board
        player = brd.player  # get our player number
        top_node = heuristic.Heuristic((brd, -1), player)  # create top node of tree
        hu = self.create_heuristic(top_node, self.max_depth, player)  # recursively build tree

        (score, path) = self.alpha_beta(hu, self.max_depth, -math.inf, math.inf, True)  # run alpha beta on huristic


        if(debug_level>=2):

            print("\033[1;37;40m \033[2;37:40m ---SELECTING PATH--------------------------------------------------------")

            print("PATH[]", path)
        return path[1]  # return the path(colum choice) of one layer deep for the high score result

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it

    def alpha_beta(self, node: heuristic.Heuristic, depth: int, a: float, b: float, maximizing_player: int) -> Tuple[
        float, List[int]]:
        """alpha beta alg to search heuristic tree"""

        '''
        originally called on the root node, with true.
        Which means, that it recurses exactly once, with FALSE
        returning node.score of play after one move (since the root node, though having encoded a col value,
        means effectively nothing and should be ignored).
        
        '''

        # If we've reached end of exploration, returns this nodes individual score and just the move made to get here
        if depth == 0 or (not node.has_children()):
            return node.score, [node.col]  # return tuple of score and path array

        # Whether we are doing minimizing or maximizing of score
        if maximizing_player:
            value = -math.inf
            value_path = []
            for child in node.children:
                # Recursively call
                child_score, child_path = self.alpha_beta(child, depth - 1, a, b, False)

                # If we find a better score, save its path as the current best
                if child_score > value:
                    value = child_score
                    value_path = child_path

                # Update alpha
                a = max(a, value)

                # Do alpha beta pruning
                if a >= b:
                    break  # beta cutoff - return early
                # if abs(child.calc_move_score(child.board,child.col))>threshold*(depth-depth+1):
                #     print("THING")
                #     break#break early if game is won

            return value, [node.col] + value_path
        else:
            value = math.inf
            value_path = []
            for child in node.children:
                # Recursively call
                child_score, child_path = self.alpha_beta(child, depth - 1, a, b, True)

                # If we find a better (IE worse) score, save its path as the current best
                if child_score < value:
                    value = child_score
                    value_path = child_path

                # Update beta
                b = min(b, value)

                # Do alpha beta cut off
                if a >= b:
                    break  # Alpha cutoff - return early
                # if abs(child.calc_move_score(child.board,child.col))>threshold*(depth-depth+1):
                #     print("THING")
                #     break#break early if game is won

            return value, [node.col] + value_path

    def create_heuristic(self, node: heuristic.Heuristic, depth: int, root: int) -> heuristic.Heuristic:
        """recursively builds tree to specified depth"""
        if depth > 0:
            # If we're calling this we want to force (re)generation
            node.children = []
            successors = self.get_successors(node.board)
            for board_and_col in successors:
                # Make a new heuristic containing the new board, the col dropped to form it, and the player1
                child = heuristic.Heuristic(board_and_col, root, node.score)
                node.add_child(child)  # , root)
                self.create_heuristic(child, depth - 1, root)

        # Regardless, return the node
        return node  # if depth zero is reached return the tree that was input

    def get_successors(self, brd: Board) -> List[Tuple[Board, int]]:
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
            succ.append((nb, col))
        return succ


THE_AGENT = AlphaBetaAgent("GamarraNikolas", 5)
