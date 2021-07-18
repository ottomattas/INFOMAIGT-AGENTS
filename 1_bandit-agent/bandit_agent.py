# Put your name and student ID here before submitting!
# Otto Mättas (6324363)

import game as g
from random_agent import RandomAgent

import random, copy, time
import numpy as np
import sys
sys.setrecursionlimit(100000)

class BanditAgent:
    def __init__(self, timelimit, id):
        self.timelimit = timelimit
        self.id = id

    def make_move(self, g):
        start = time.perf_counter()
        epsilon = 0
        
        # run until time is up
        while time.perf_counter() - start < self.timelimit / 1000:
            # print(epsilon)
            # free_positions = g.board.random_free()
            # print(free_positions)
            # break

            # start rollout
            
            # if epsilon < random.value, then explore
            if random.random() > epsilon:
                # Copy the board for simulation
                b = copy.deepcopy(g.board)
                print("Deepcopy of the board is \n", b)

                # Check the free positions
                free_positions = g.board.free_positions()
                print("Free positions are \n", free_positions)

                # Choose a random next action
                next_move = random.choice(free_positions)
                print("Random next_move is", next_move)

                # Take the action on the copied board
                b.place(next_move, 1)
                print("Action has been taken as the board shows \n", b)

                # Set parameters for the simulation game
                # Use two random agents and the deepcopy of the board
                simulation_players = [RandomAgent(1), RandomAgent(2)]
                g.from_board(b, g.objectives, simulation_players, g.print_board)
                print("The return of the from_board is \n", b, g.objectives, simulation_players, g.print_board)

                # Run the game, player who won is returned
                g.play()
                print("Returned player from game:", player)
                
                    # if player 1 , add position_value +1
                    #if g.player.id == 1:
                        #position_value =+ 1

                    # if player 2, add position_value 0
                    #elif g.player.id == 2:
                        #position_value =+ 0

                    # if draw, add position_value 0.5
                    #else:
                        #position_value =+ 0,5
                    # position_counter=+ #how many times was this position chosen

                    #position_counter =+ 1

            # calculate the average position_value / position_counter, then update the array of chances of winning for the board                

            # if epsilon => random.value, then exploit
            if random.random() <= epsilon:
                # Copy the board for simulation
                b = copy.deepcopy(g.board)
                print("Deepcopy of the board is", b)

                # Check the free positions
                free_positions = g.board.free_positions()
                print("Free positions are", free_positions)

                # Choose a random next action
                start_position = random.choice(free_positions)
                print("Random start position is", start_position)

                # Take the action on the copied board
                b.place(start_position, 1)
                print("Action has been taken as the board shows:", b)

                # create a new game instance (play) using two random agents and the deepcopied board (from_board)
                g.from_board(b, g.objectives, g.players, g.print_board)
                # print("Instantiate a new board for play: ", b)
                # print("Instantiate objectives for play: ", g.objectives)
                # print("Instantiate players for play: ", g.players)
                # print("Instantiate print_board for play: ", g.print_board)

                # game finishes, player who won is returned
                g.play()
                print("Returned player from game:", player)
                break
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
