# Put your name and student ID here before submitting!
# Otto Mättas (6324363)

import game as g
from random_agent import RandomAgent

import random
import copy
import time
import numpy as np

class BanditAgent():
    def __init__(self, timelimit, id):
        self.timelimit = timelimit
        self.id = id

    def make_move(self, g):
        start = time.perf_counter()
        start_epsilon = 1.0
        end_epsilon = 0.0
        number_of_possible_moves = len(g.board.free_positions())
        
        # Create array for possible epsilon values
        epsilon_array = np.linspace(start_epsilon, end_epsilon, self.timelimit)
        #print("Epsilon decay list:", epsilon_array)

        # Create arrays for evaluating the position
        position_win_probability = np.zeros(number_of_possible_moves)
        position_score = np.zeros(number_of_possible_moves)
        position_counter = np.zeros(number_of_possible_moves)

        # run until time is up
        while time.perf_counter() - start < self.timelimit / 1000:
            
            # Check for free positions
            free_positions = g.board.free_positions()
            #print("Free positions:\n", free_positions)

            #################
            # Start rollout #
            #################

            # Copy the board for simulation
            b = copy.deepcopy(g.board)
            #print("Deepcopy:\n", b)

            # Create an index for the move
            index = random.randrange(0, len(free_positions))

            # Set epsilon
            epsilon = epsilon_array[0]
            print("Epsilon: ", epsilon)

            if epsilon != 0:
                # Remove the used epsilon for decay
                epsilon_index = np.where(epsilon_array == epsilon)[0][0]
                epsilon_array = np.delete(epsilon_array, epsilon_index)
                #print("Epsilon array after last delete: ", epsilon_array)
                
            # Select a greedy move
            if random.random() > epsilon:
                # Create a tuple to find the list of highest probabilities
                highest_probabilities = np.where(position_win_probability == np.amax(position_win_probability))
                #print('Returned tuple of highest probabilities :', highest_probabilities)
                
                # Save the list of indices for those highest probabilities
                highest_probabilities_indices = highest_probabilities[0]
                #print('List of Indices of highest probabilities :', highest_probabilities_indices)
                
                # Extract the first index for the highest probabilities from
                # the list as there might be more than one highest probability
                highest_probability_index = highest_probabilities_indices[0]
                #print("Highest probability index is", highest_probability_index)
                
                # Select the move
                selected_move = free_positions[highest_probability_index]
                print("Selected greedy move:", selected_move)

            # Select a random move
            else:
                # Select a random move
                selected_move = free_positions[index]
                print("Selected random move:", selected_move)

            # Take the move on the copied board
            b.place(selected_move, self.id)

            # Set parameters for simulation
            simulation_players = [RandomAgent(1), RandomAgent(2)]
            simulation_game = g.from_board(b, g.objectives, simulation_players, g.print_board)

            # Simulate and determine the winner
            winner = simulation_game.play()
            #print("Simulation END:\n", b, "\nWinner is: ", winner)
            
            # Give values to states
            # winner==True
            if winner:
                # if player 1 , value 1
                if winner.id == 1:
                    position_score[index] += 1
                    #print("position_score after win", position_score[index])

                # if player 2, value -1
                else:
                    position_score[index] -= 1
                    #print("position_score after loss", position_score[index])
            # winner==False
            else:
                # if draw, value 0
                position_score[index] += 0
                #print("position_score after draw", position_score[index])

            # Count the times a position is visited
            position_counter[index] += 1
            #print("position_counter is", position_counter[index])

            # Calculate average position value
            position_win_probability[index] = position_score[index] / position_counter[index]
            #print("Average value is", position_win_probability[index])

        # return the best move you've found here
        #print("GIVE THE MOVE BACK TO THE ACTUAL GAME:", selected_move)
        #print("probability:", selected_move)
        return selected_move
        #return g.board.random_free()

    def __str__(self):
        return f'Player {self.id} (BanditAgent)'
