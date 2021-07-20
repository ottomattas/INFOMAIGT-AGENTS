#! /usr/bin/env -S python -u
from game import Game
from random_agent import RandomAgent
from neural_network_agent import NNAgent

import argparse, time, cProfile
import numpy as np
import multiprocessing as mp
from collections import Counter
from itertools import starmap
import tensorflow as tf

def main(args):
    if args.input:

        # Load dataset
        data = read_games(args.input)
        #print("Game 1 array is \n", data[0])

        # Count the board states
        board_state_count = 0
        # For each _ element, and game element
        for _, game in data:
            # For each _ element as only the number of elements is relevant
            for _, _, _ in game:
                board_state_count += 1
                #print("Board state count is ",board_state_count)

        # Create array for the input layer
        # (Columns: each possible move, represented in one-hot encoding
        # Rows: each possible board state)
        x_train = np.zeros((board_state_count,75),dtype=int)
        #print("X train is \n",x_train)

        # Create array for the output layer
        # (For each board state, save the winner)
        y_train = np.zeros(board_state_count,dtype=int)
        #print("Y train is \n",y_train)

        # Create indexes for game and board
        game_index = 0
        board_index = 0

        # Loop over all games and boards
        for winner, game in data:
            game_index += 1
            for player, move, board in game:
                #print("Player is ", player)
                #print("Move is ", move)
                #print("Board is\n", board)
                #print("Winner is ", winner)

                ##########################
                # Create the input layer #
                ##########################
                # For each player, we want to look it from their perspective.
                # Set each player's move as 0 0 1 in x_train.

                # Define a list for appending the one-hot encoded players    
                lst = []

                # If player 1 move
                if player == 1:
                    for x in range(5):
                        for y in range(5):
                            # When position value is 1 (player 1 move)
                            if board[x, y] == 1:
                                # Append 0 0 1
                                lst.append(0)
                                lst.append(0)
                                lst.append(1)
                            # When position value is 2 (player 2 move)
                            elif board[x, y] == 2:
                                # Append 0 1 0
                                lst.append(0)
                                lst.append(1)
                                lst.append(0)
                            # When position value is 0 (no player move yet)
                            else:
                                # Append 1 0 0
                                lst.append(1)
                                lst.append(0)
                                lst.append(0)
                    # Save the one-hot encoded list in the x_train array
                    # at position board_index
                    x_train[board_index] = np.array(lst)
                    #print("After player 1 move, encoded board is now \n", x_train[board_index])
                    #print("After player 1 move, x_train is now \n", x_train)
                
                # If player 2 move
                else:
                    for x in range(5):
                        for y in range(5):
                            # When position value is 2 (player 2 move)
                            if board[x, y] == 2:
                                # Append 0 0 1
                                lst.append(0)
                                lst.append(0)
                                lst.append(1)
                            # When position value is 1 (player 1 move)
                            elif board[x, y] == 1:
                                # Append 0 1 0
                                lst.append(0)
                                lst.append(1)
                                lst.append(0)
                            # When position value is 0 (no player move yet)
                            else:
                                # Append 1 0 0
                                lst.append(1)
                                lst.append(0)
                                lst.append(0)
                    # Save the one-hot encoded list in the x_train array
                    # at position board_index
                    x_train[board_index] = np.array(lst)
                    #print("After player 2 move, encoded board is now \n", x_train[board_index])
                    #print("After player 2 move, x_train is now \n", x_train)


                ###########################
                # Create the output layer #
                ###########################
                # If draw
                if winner == 0:
                    y_train[board_index] = 0
                # If player 1 is winner
                elif winner == player:
                    y_train[board_index] = 1
                # If player 2 is winner
                else:
                    y_train[board_index] = 2

                #print("y_train is", y_train)

                board_index += 1
                #print("This is game nr: ", game_index, "\nThis is board nr: ", board_index)                    

        # ############
        # # Training #
        # ############
        # # Create the tf.keras.Sequential model by stacking layers.
        # # Choose an optimizer and loss function for training.
        # model = tf.keras.models.Sequential([
        # tf.keras.layers.InputLayer(input_shape=(75)), # We have an array with 75 objects
        # tf.keras.layers.Dense(2000, activation='relu'),
        # tf.keras.layers.Dense(2000),
        # tf.keras.layers.Dense(2000),
        # tf.keras.layers.Dropout(0.2),
        # tf.keras.layers.Dense(3, activation='softmax') # We have only win/loss/draw, so value is 3
        # ])

        # # # # Compile the model
        # model.compile(optimizer='adam',
        #             loss='sparse_categorical_crossentropy', # look at that
        #             metrics=['accuracy'])
        
        # # # # Adjust the model parameters to minimize the loss
        # model.fit(x_train, y_train, epochs=1)

        # # Checks the models performance
        # #model.evaluate(x_test, y_test, verbose=2)

        # # Save the model     
        # model.save("nn1_model", overwrite=False)

    work = []
    for i in range(args.games):
        # swap order every game
        if i % 2 == 0:
            players = [NNAgent(1), RandomAgent(2)]
        else:
            players = [RandomAgent(2), NNAgent(1)]

        work.append((args.size,
                     read_objectives(args.objectives),
                     players,
                     args.output,
                     args.print_board))

    start = time.perf_counter()

    # the tests can be run in parallel, or sequentially
    # it is recommended to only use the parallel version for large-scale testing
    # of your agent, as it is harder to debug your program when enabled
    if args.parallel == None or args.output != None:
        results = starmap(play_game, work)
    else:
        # you probably shouldn't set args.parallel to a value larger than the
        # number of cores on your CPU, as otherwise agents running in parallel
        # may compete for the time available during their turn
        with mp.Pool(args.parallel) as pool:
            results = pool.starmap(play_game, work)

    stats = Counter(results)
    end = time.perf_counter()

    print(f'Total score {stats[1]}/{stats[2]}/{stats[0]}.')
    print(f'Total time {end - start} seconds.')

def play_game(boardsize, objectives, players, output, print_board = None):
    game = Game.new(boardsize, objectives, players, print_board == 'all')

    if output:
        with open(output, 'a') as outfile:
            print(boardsize, file = outfile)
            winner = game.play(outfile)
            print(f'winner={winner.id if winner else 0}', file = outfile)
    else:
        winner = game.play()

    if print_board == 'final':
        game.print_result(winner)

    return 0 if winner == None else winner.id

def read_objectives(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file]

    i = 0
    shapes = []
    while i < len(lines):
        shape = []

        # shapes are separated by blank lines
        while i < len(lines) and lines[i].strip() != '':
            shape_line = []
            for char in lines[i].strip():
                shape_line.append(char == 'x')
            shape.append(shape_line)
            i += 1

        shapes.append(np.array(shape))
        i += 1

    return shapes

def read_games(filename):
    with open(filename) as file:
        lines = list(file)

        games = []

        i = 0
        while i < len(lines):
            game = []
            boardsize = int(lines[i])
            i += 1

            while not lines[i].startswith('winner'):
                turn = int(lines[i])
                i += 1
                move = [int(x) for x in lines[i].split(',')]
                i += 1
                board = np.zeros((boardsize, boardsize), dtype = int)
                for y in range(boardsize):
                    row = lines[i].split(',')
                    for x in range(boardsize):
                        board[(x, y)] = int(row[x])
                    i += 1
                game.append((turn, move, board))

            winner = int(lines[i].split('=')[1])
            games.append((winner, game))
            i += 1

        return games

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--size', type = int, default = 10,
        help = 'The size of the board.')

    parser.add_argument('--games', type = int, default = 1,
        help = 'The number of games to play.')

    parser.add_argument('--time', type = int, default = 10,
        help = 'The allowed time per move, in milliseconds.')

    parser.add_argument('--print-board', choices = ['all', 'final'],
        help = 'Show the board state, either every turn or only at the end.')

    parser.add_argument('--parallel', type = int,
        help = 'Run multiple games in parallel. Only use for large-scale '
        'testing.')

    parser.add_argument('--output',
        help = 'Write training data to the given file.')

    parser.add_argument('--input',
        help = 'Read training data from the given file.')

    parser.add_argument('objectives',
        help = 'The name of a file containing the objective shapes. The file '
        'should contain a rectangle with x on positions that should be '
        'occupied, and dots on other positions. Separate objective shapes '
        'should be separated by a blank line.')

    args = parser.parse_args()
    #cProfile.run('main(args)')
    main(args)
