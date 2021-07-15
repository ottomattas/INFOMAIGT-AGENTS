'''Finally, a small hint: your agent will need to do a lot of simulations
based on a random agent. It just so happens that a random agent is already
implemented, as it is the opponent you will be playing against.
An easy way to simulate a game is to create a copy of the board (look up 
how to create a deep copy in Python, to avoid modifying the original
 unintentionally) and then use the Game.from_board method to create 
 a new game from the given board state, using two new random agents. 
 Then you can just play the game by calling Game.play(), 
 which returns the agent that won the game, or None if it was a tie.

            Saul:
            
            There is a board state, which states the value of each square on the grid

            In this board state, there are some squares with no value left. 
            These are the moves that the agent could possibly make
                
            For as much time as possible (the timelimit), 
            the agent wants to try to determine which of those empty squares is the best move to make
                
            The best move to make with these squares is the move that yields the highest chance of a win
            ------- 
            What this pretty much means is that for each possible move,
            we create a new 'temp game' in which this move has been made.
            
            We then check who wins this new temp game if both players keep making random moves
                
            When the timelimit has been reached, the agent will return the move that has the highest chance of winning'''

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

    def make_move(self, g):
        start = time.perf_counter()

        # run until time is up
        while time.perf_counter() - start < self.timelimit / 1000:
            # replace the line below with your actual implementation!
            break

        # return the best move you've found here
        return g.board.random_free()

    def __str__(self):
        return f'Player {self.id} (BanditAgent)'
