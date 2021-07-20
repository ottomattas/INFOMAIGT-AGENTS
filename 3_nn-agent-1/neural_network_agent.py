# Put your name and student ID here before submitting!
# Otto Mättas (6324363)

import random
import numpy as np
import copy

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
        #print("Free positions are:\n", free_positions)

        # Define an array for storing all the one-hot encoded board states
        arr = np.zeros((len(free_positions),75),dtype=int)

        # Define a board counter
        board_counter = 0

        ############
        # Simulate #
        ############
        # For each free position
        for move in free_positions:

            # Copy the board for simulation
            b = copy.deepcopy(game.board)

            # Take the move on the copied board
            b.place(move, self.id)

            # Loop over the whole board with the size 5x5
            for x in range(5):
                for y in range(5):

                    # Update the array with the encoding
                    # Each value gets a one-hot encoding, so the translations
                    # can be made as follows:
                    # value 0 -> 1 0 0
                    # value this player (self.id) -> 0 0 1
                    # value other player -> 0 1 0

                    # When position value is 0 (no player move yet)
                    if b.value((x, y)) == 0:

                        # Find position for the empty space and update it
                        arr[board_counter,(y*3)+(x*15)] = 1

                    # When current agent makes move
                    elif b.value((x, y)) == self.id:

                        # Find position and update for one-hot encoding
                        arr[board_counter,(y*3)+(x*15)+2] = 1

                    # Then the other agent makes move
                    else:

                        # Find position and update for one-hot encoding
                        arr[board_counter,(y*3)+(x*15)+1] = 1   

            # Count the board
            board_counter += 1

        ###########
        # Predict #
        ###########
        # Create variables for current best move probability
        current_best_move_probability = -1

        # Define a move counter
        move_counter = 0

        # Generate winning predictions for all board states
        predictions = self.model.predict(arr)
        #print("Predictions:\n", predictions)

        # For each prediction
        for prediction in predictions:

            # If the current probability is lower than the prediction (win+draw)
            if current_best_move_probability < (prediction[1] + prediction[0]):

                # Update the current best move win probability
                current_best_move_probability = (prediction[1] + prediction[0]) 

                # Update the current best move
                current_best_move = free_positions[move_counter]
                #print("Current best move win probability is: ", current_best_move_win_probability)
                #print("Current best move is: ", current_best_move)

            # Count a move
            move_counter += 1

        # use your neural network to make a move here
        return current_best_move
        
    def __str__(self):
        return f'Player {self.id} (NNAgent)'
