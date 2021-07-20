# Put your name and student ID here before submitting!
# Otto Mättas (6324363)

import random
import numpy as np

# uncomment one of the two lines below, depending on which library you want to use
import tensorflow as tf
# import torch


class NNAgent:
    def __init__(self, id):
        self.id = id
        # initialise your neural network here
        self.model = tf.keras.models.load_model("nn1_model")

    def make_move(self, game):

        # Check for free positions
        free_positions = game.board.free_positions()
        print("Free positions are:\n", free_positions)

        # Create variables for current best move
        current_best_move = 0
        current_best_move_win_probability = -1

        # For each free position
        for move in free_positions:

            # Copy the board for simulation
            b = copy.deepcopy(game.board)

            # Take the move on the copied board
            b.place(move, self.id)

            # Define a list for appending the one-hot encoded players    
            lst = []

            # Loop over the whole board and append one-hot encoding value
            for x in range(5):
                for y in range(5):

                    # When position value is 0 (no player move yet)
                    if b.value((x, y)) == 0:
                        # Append 1 0 0
                        lst.append(1)
                        lst.append(0)
                        lst.append(0)

                    # When this agent makes move
                    elif b.value((x, y)) == self.id:
                        # Append 0 0 1
                        lst.append(0)
                        lst.append(0)
                        lst.append(1)
                    # Then the other agent makes move
                    else:
                        # Append 0 1 0
                        lst.append(0)
                        lst.append(1)
                        lst.append(0)

            # Save the one-hot encoded list as a new 2D numpy array
            b_one_hot = np.array([lst])
            #print("Shape of the deepcopy one-hot board state: ", b_one_hot.shape)
            #print("Deepcopy one-hot board state \n", board_state_one_hot)

            # Generate winning predictions for board state
            predictions = self.model.predict(b_one_hot)
            #print("Predictions:\n", predictions)

            # Check if the current move has the highest win probability
            if current_best_move_win_probability < predictions[0,1]:

                # Update the current best move win probability
                current_best_move_win_probability = predictions[0,1]
            
                # Update the current best move
                current_best_move = move
                #print("Current best move win probability is: ", current_best_move_win_probability)
                #print("Current best move is: ", current_best_move)

        # use your neural network to make a move here
        return game.board.random_free()
        #return best_move
        

    def __str__(self):
        return f'Player {self.id} (NNAgent)'
