from board import Board

import numpy as np

class Game:
    def __init__(self, board, objectives, players, print_board):
        self.board = board
        self.objectives = objectives
        self.players = players
        self.print_board = print_board

    @classmethod
    def new(cls, boardsize, objectives, players, print_board):
        board = Board(boardsize)
        return cls(board, objectives, players, print_board)

    @classmethod
    def from_board(cls, board, objectives, players, print_board):
        return cls(board, objectives, players, print_board)

    def play(self):
        draw = False
        while not draw:
            for player in self.players:
                if self.board.full():
                    draw = True
                    break

                pos = player.make_move(self)
                if not self.board.is_free(pos):
                    print(f'Illegal move attempted!'
                          f'Position ({pos[0]}, {pos[1]}) is not free.')
                    return None

                self.board.place(pos, player.id)
                if self.print_board:
                    print(self.board)

                if self.victory(pos, player.id):
                    return player

        return None

    # tests whether player with given id has made the given shape by placing
    # a marker at hint position
    def victory(self, hint, playerid):
        xh, yh = hint

        for shape in self.objectives:
            for xo in range(shape.shape[0]):
                for yo in range(shape.shape[1]):
                    if not shape[xo, yo]:
                        continue

                    if xo > xh or yo > yh:
                        continue

                    if (shape.shape[0] - xo > self.board.shape[0] - xh) or \
                       (shape.shape[1] - yo > self.board.shape[1] - yh):
                        continue

                    fits = True
                    for x in range(shape.shape[0]):
                        for y in range(shape.shape[1]):
                            if not shape[x, y]:
                                continue

                            pos = (xh - xo + x, yh - yo + y)
                            if self.board.value(pos) != playerid:
                                fits = False
                                break

                        if not fits:
                            break

                    if fits:
                        return True

        return False

    def print_result(self, player = None):
        if player == None:
            print('Draw!')
        else:
            print(f'{player} wins!')
        print(self.board, flush = True)
