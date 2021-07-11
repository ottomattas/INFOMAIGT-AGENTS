# Put your name and student ID here before submitting!
# Otto Mättas (6324363)

from random_agent import RandomAgent

import time

class MCTSAgent:
    def __init__(self, timelimit, id):
        self.timelimit = timelimit
        self.id = id

    def make_move(self, game):
        start = time.perf_counter()

        # run until time is up
        while time.perf_counter() - start < self.timelimit / 1000:
            # do MCTS on top of RandomAgent here
            break

        return game.board.random_free()

    def __str__(self):
        return f'Player {self.id} (MCTSAgent)'