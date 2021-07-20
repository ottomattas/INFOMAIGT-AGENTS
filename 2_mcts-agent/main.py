#! /usr/bin/env -S python -u
from game import Game
from random_agent import RandomAgent
from score_agent import ScoreAgent
from mcts_agent import MCTSAgent

import argparse, time
import numpy as np
import multiprocessing as mp
from collections import Counter
from itertools import starmap

def main(args):
    work = []
    for i in range(args.games):
        # swap order every game
        if i % 2 == 0:
            players = [MCTSAgent(args.time, 1), RandomAgent(2)]
        else:
            players = [RandomAgent(2), MCTSAgent(args.time, 1)]

        work.append((args.size,
                     read_objectives(args.objectives),
                     players,
                     args.print_board))

    start = time.perf_counter()

    # the tests can be run in parallel, or sequentially
    # it is recommended to only use the parallel version for large-scale testing
    # of your agent, as it is harder to debug your program when enabled
    if args.parallel == None:
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

def play_game(boardsize, objectives, players, print_board = None):
    game = Game.new(boardsize, objectives, players, print_board == 'all')
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

        shapes.append(np.transpose(np.array(shape)))
        i += 1

    return shapes

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

    parser.add_argument('objectives',
        help = 'The name of a file containing the objective shapes. The file '
        'should contain a rectangle with x on positions that should be '
        'occupied, and dots on other positions. Separate objective shapes '
        'should be separated by a blank line.')

    args = parser.parse_args()
    main(args)
