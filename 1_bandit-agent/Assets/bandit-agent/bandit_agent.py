# Put your name and student ID here before submitting!
# Name (student ID)

import game as g
from random_agent import RandomAgent

import random, copy, time
import numpy as np

class BanditAgent:
    def __init__(self, timelimit, id):
        self.timelimit = timelimit
        self.id = id

    def make_move(self, game):
        start = time.perf_counter()

        # run until time is up
        while time.perf_counter() - start < self.timelimit / 1000:
            # replace the line below with your actual implementation!
            break

        # return the best move you've found here
        return game.board.random_free()

    def __str__(self):
        return f'Player {self.id} (BanditAgent)'
