import random
import game
import agent
import alpha_beta_agent as aba

from GamarraNikolas.alpha_beta_agent import THE_AGENT as GamarraNikolas
from GamarraNikolas2.alpha_beta_agent import THE_AGENT as GamarraNikolas2
from GamarraNikolas3.alpha_beta_agent import THE_AGENT as GamarraNikolas3

from LessardPhilippe.alpha_beta_agent import THE_AGENT as LessardPhilippe
from GumiennyKamil.alpha_beta_agent import THE_AGENT as GumiennyKamil

# Set random seed for reproducibility
random.seed(1)


g = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
              GamarraNikolas2,  # player 1
              GamarraNikolas3)       # player 2
#
# Random vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.RandomAgent("random1"),       # player 1
#               agent.RandomAgent("random2"))       # player 2

#
# Human vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               agent.RandomAgent("random"))        # player 2

#
# Random vs. AlphaBeta
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.RandomAgent("random"),        # player 1
#               aba.AlphaBetaAgent("alphabeta", 4)) # player 2

#
# Human vs. AlphaBeta
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               aba.AlphaBetaAgent("alphabeta", 4)) # player 2

#
# Human vs. Human
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human1"),   # player 1
#               agent.InteractiveAgent("human2"))   # player 2

# Execute the game
outcome = g.go()
