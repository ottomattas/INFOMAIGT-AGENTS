import random
import numpy as np

class Board:
    def __init__(self, size):
        self.board = np.zeros((size, size), dtype = int)
        self.shape = self.board.shape

    # test if the given position is free
    def is_free(self, pos):
        return self.value(pos) == 0

    # returns the value at the given position
    def value(self, pos):
        return self.board[pos[0], pos[1]]

    # returns all free positions
    def free_positions(self):
        return np.argwhere(self.board == 0)

    # tests if the board is full
    def full(self):
        return np.all(self.board)

    # place the given value at the given position
    def place(self, pos, playerid):
        self.board[pos[0], pos[1]] = playerid

    # returns a random free position
    def random_free(self):
        while True:
            x = random.randrange(0, self.shape[0])
            y = random.randrange(0, self.shape[1])

            if self.is_free((x, y)):
                return (x, y)

    def output_state(self, file):
        for y in range(self.board.shape[1]):
            row = [str(self.board[(x, y)]) for x in range(self.board.shape[0])]
            print(','.join(row), file = file)

    def __str__(self):
        symbol_map = { 0: ' ', 1: 'O', 2: 'X'}

        lines = []
        lines.append('-' * (self.board.shape[0] + 2))
        for y in range(self.board.shape[1]):
            row = '|'
            for x in range(self.board.shape[0]):
                row += symbol_map[self.board[x, y]]
            row += '|'

            lines.append(row)

        lines.append('-' * (self.board.shape[0] + 2))

        return '\n'.join(lines)
