# Put your name and student ID here before submitting!
# Otto Mättas (6324363)

import game as g
from random_agent import RandomAgent

import random, copy, time
import numpy as np

class BanditAgent:
    def __init__(self, timelimit, id):
        self.timelimit = timelimit
        self.id = id
        self.epsilon = 0

    def make_move(self, g, epsilon):
        start = time.perf_counter()

        # run until time is up
        while time.perf_counter() - start < self.timelimit / 1000:
            # replace the line below with your actual implementation!
            #break

            # start rollout

                # if epsilon < random.value, then explore
                if epsilon < random() :

                    # look at possible actions, choose random one
                    next_move = g.board.random_free()
                    print(next_move)

                        # do the move on the deepcopy of the board
                        

                                # create a new game instance (play) using two random agents and the deepcopied board (from_board)
                                
                                # game finishes, player who won

                                # if player 1 , add position_value +1

                                # if player 2, add position_value 0

                                # if draw, add position_value 0.5

                                # position_counter=+ #how many times was this position chosen

                    # calculate the average position_value / position_counter, then update the array of chances of winning for the board                

                # if epsilon => random.value, then exploit

                    # look at possible actions, choose best one (randomly if equal bests)

                            # do the move on the deepcopy of the board
                                # create a new game instance (play) using two random agents and the deepcopied board (from_board)
                                
                                # game finishes, player who won

                                # if player 1 , add position_value +1

                                # if player 2, add position_value 0

                                # if draw, add position_value 0.5

                                # position_counter=+ #how many times was this position chosen

                    # calculate the average position_value / position_counter, then update the array of chances of winning for the board
            
                # when time passes, grow epsilon. curve vs linear

        # return the best move you've found here
        return g.board.random_free()

    def __str__(self):
        return f'Player {self.id} (BanditAgent)'
