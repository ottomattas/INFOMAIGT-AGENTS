# Put your name and student ID here before submitting!
# Otto Mättas (6324363)

import random

# uncomment one of the two lines below, depending on which library you want to use
# import tensorflow
# import torch

class NNAgent:
    def __init__(self, id):
        self.id = id
        # initialise your neural network here

    def make_move(self, game):
        # use your neural network to make a move here
        return game.board.random_free()

    def __str__(self):
        return f'Player {self.id} (NNAgent)'
