import math
from typing import List, Tuple

from agent import Agent
from board import Board
from . import MCTS

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# from . import Heuristic

debug_level=0
threshold=9000


###########################
# Alpha-Beta Search Agent #
###########################
class AlphaZeroAgent(Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth


    def train(self,brd, t):

    def get_action(self,policy):
        max_value = max(policy)
        return   policy.index(max_value)


    def go(self, brd):  # main routine invoked by game simulator

        player = brd.player  # get our player number
        top_node = MCTS.Heuristic((brd, -1), player)  # create top node of tree
        hu = self.create_heuristic(top_node, self.max_depth, player)  # recursively build tree

        policy = get_policy(brd, t) # Ask our saved neural net the optimal choice



        return policy  # return the path(colum choice) of one layer deep for the high score result



    def encode_board(self,brd):
    board_state = brd.current_board
    encoded = np.zeros([6,7,3]).astype(int)
    encoder_dict = {"O":-1, "X":1,"1":1, "2":-1}
    for row in range(6):
        for col in range(7):
            if board_state[row,col] != " ":
                encoded[row, col, encoder_dict[board_state[row,col]]] = 1
    if board.player == 1:
        encoded[:,:,2] = 1 # player to move
    return encoded

    def invert_board(self,brd):
        return -1*brd;


THE_AGENT = AlphaZeroAgent("AlphaZeroAgent", 4)
