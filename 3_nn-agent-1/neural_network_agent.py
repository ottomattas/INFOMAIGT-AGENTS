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
        # OPTION 1
        # For each possible action
        # Return the first move as best_move
        # If the second move is with a better prediction, update the best_move etc

        # OPTION 2
        # Give a one-hot encoded boardstate to model
        # Ask model to give prediction on draw/win/loss
        # Choose the boardstate with the highest probability for win
        # Return the boardstate

        # Check for free positions
        free_positions = game.board.free_positions()
        print("Free positions are:\n", free_positions)

        # Create variable for best_move
        best_move = 0

        # Create an array for prediction samples
        samples_to_predict = []

        print("x_train is: \n", self.x_train)

        # For each free position
        for move in free_positions:
            # Add sample to array for prediction
            samples_to_predict.append(x_train[move])

            # Convert into Numpy array
            samples_to_predict = np.array(samples_to_predict)
            print("Samples to predict array:\n", samples_to_predict)
            #print(samples_to_predict.shape)

            # Generate predictions for samples
            predictions = self.model.predict(samples_to_predict)
            print("Predictions:\n",predictions)
            
            # Generate arg maxes for predictions
            classes = np.argmax(predictions, axis = 1)
            print(classes)

        # use your neural network to make a move here
        return game.board.random_free()
        #return best_move
        

    def __str__(self):
        return f'Player {self.id} (NNAgent)'
